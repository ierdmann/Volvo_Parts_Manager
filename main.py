from flask import Flask, render_template, request, send_file
from lib import NewDataBase, InsertData, FetchDataBase, UpdateDatabase, DeleteFromDatabase, IpReader, sendMail, orderStatus, date, FreeSqlOrder
import os
from openpyxl import Workbook


try:
	dateNow = date()
	database_parts = "parts.db" #Teile Datenbank
	database_part_info = "partsInfo.db"  #Teile Informationen Datenbank
	database_part_order = "partOrder.db" #Datenbank für Teilebestellungen
	table_parts = "parts"                #Tabelle für Teile Datenbank
	table_part_info = "Info"             #Tabelle für Teile Info Datenbank
	table_order = "partsorder"			#Tabelle für Datenbank für Teile Bestellungen
	data_typs= "id INTEGER PRIMARY KEY, orders INT, job INT, part text, amounts real, OrderDate text"
	first_value = f"6902578, 1, 'VO 698996', 2.3, '{dateNow}'"
	receive_mail = "ilmarinenerdmann@freenet.de"
	subject = "Die IP Adresse nach dem Start"
	header_mail = "Der Raspberry wurde neugestartet!"
	mail_message = f"Die aktuelle IP-Adresse lautet: {IpReader()}:5000"


	sendMail(receive_mail, subject, header_mail, mail_message)

	if f"{database_parts}" in os.listdir("../pythonProject/"):
		print(f"Datenbank [{database_parts}] vorhanden!")
	else:
		NewDataBase(database_parts, table_parts, data_typs)

	#InsertData(databasename, tablename, firstValue) erster eintrag in Datenbank parts.db

	app = Flask(__name__, static_folder='OrderPrintLists')

	@app.route('/all')
	def all_order():
		orders = []
		orders = [print(a[1]) if a[1] in orders else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} ORDER BY orders")]
		parts = [print(a[1]) if a[1] in orders else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} ORDER BY orders")]
		for a in parts:
			print(a)
		checkbox = request.args.getlist("checkbox")
		if checkbox != None and len(checkbox) > 0:
			print(checkbox[0])
		for box in checkbox:
			DeleteFromDatabase(database_parts, table_parts, box)
		return render_template("table.html", content=len(parts), parts=parts)

	@app.route("/")
	def index():
		order_del = request.args.getlist("Auftrag_löschen")
		print(order_del)
		order = [a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} ORDER BY orders")]
		content = []
		memory = ""
		for a in order:
			if memory == a[1]:
				continue
			else:
				content.append(a)
				memory = a[1]
		for delet in order_del:
			comand = f"DELETE FROM {table_parts} WHERE orders={delet}"
			FreeSqlOrder(database_parts, table_parts, comand)
			print(f"Der Auftrag {delet} wurde gelöscht!")
		return render_template("over_view.html", content=len(content), parts=content)

	# Vielleicht löschen
	@app.route('/order')
	def order():
		date_now = date()
		order_nr = request.args.get("Auftragsnummer")
		job_nr = request.args.get("Jobnummer")
		part_nr = request.args.get("Teilenummer")
		amounts_nr = request.args.get("Menge")
		orderStatus(order_nr, job_nr, part_nr, amounts_nr, database_parts, table_parts, date_now)
		return render_template("order.html")

	#Vielleicht löschen
	#@app.route("/manage")
	#def manage():
	#	dateNow = date()
#		order = [0]
#		search = request.args.get("search")
#		ordernr = request.args.get("Auftragsnummer")
#		if ordernr != None:
#			print(f"Der Speicher ist {ordernr}")
#			search = ordernr
#		order = [a if a in order  else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} WHERE orders ={search} ORDER BY job")]
#		ordernr = request.args.get("Auftragsnummer")
#		job = request.args.get("Jobnummer")
#		part = request.args.get("Teilenummer")
#		amounts = request.args.get("Menge")
#		orderStatus(ordernr, job, part, amounts, database_parts, table_parts, dateNow)
#		return render_template("manageorder.html", len=len(order), order=order, table=search)

	@app.route("/landing")
	def landing():
		wire = request.args.get("Leitungen")
		long = request.args.get("Länge")
		ampere = request.args.get("Stromstärke")
		liquid = request.args.get("Leitwert")
		fall = request.args.get("Spannungsfall")
		voltage = request.args.get("Betriebsspannung")
		if (wire or long or ampere or liquid or fall or voltage) == None:
			result = 0
		else:
			wire = wire.replace(',', '.')
			long = long.replace(',', '.')
			ampere = ampere.replace(',', '.')
			liquid = liquid.replace(',', '.')
			fall = fall.replace(',', '.')
			voltage = voltage.replace(',', '.')
			result = round(((float(wire) * float(long) * float(ampere)) / (float(liquid) * (float(fall) * float(voltage)))), 2)
		return render_template("landingpage.html", ergebniss=result)

	@app.route("/job", methods=['GET'])
	def job():
		return render_template("job.html")

	@app.route("/joborder", methods=['GET'])
	def joborder():
		date_now = date()
		order_nr = request.args.get("Auftragsnummer")
		job_nr = request.args.get("Jobnummer")
		if job_nr == None:
			job_nr = 0
		part_nr = request.args.get("Teilenummer")
		amounts_nr = request.args.get("Menge")
		if order_nr == None or order_nr == "" or len(order_nr) < 7:
			message = f"{order_nr} konnte nicht gefunden werden!"
			return render_template("error.html", message=message)
		table = [a if a == order_nr else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} WHERE orders={order_nr} ORDER BY job ASC")]
		if job_nr != 0:
			orderStatus(order_nr, job_nr, part_nr, amounts_nr, database_parts, table_parts, date_now)
		return render_template("joborder.html", len=len(table), table=order_nr, jobnr=job_nr, tables=table)

	@app.route("/correct")
	def correct():
		return render_template("correct.html")

	@app.route("/correcting")
	def correcting():
		order = request.args.get("Auftragsnummer")
		id = request.args.get("checkbox")
		if order == None:
			abb = [a for a in FetchDataBase(database_parts, f"SELECT orders FROM {table_parts} WHERE id={id}")]
			order = f"{abb[0][0]}"
		if id != None:
			table = [a if a == order else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} WHERE id={id} ORDER BY job ASC")]
			return render_template("update_amounts.html", parts=table, content=len(table))
		else:
			if order != None:
				table = [a if a == order else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} WHERE orders={order} ORDER BY job ASC")]
			return render_template("correcting.html", parts=table, content=len(table))
		if order != None:
			table = [a if a == order else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} WHERE orders={order} ORDER BY job ASC")]
		return render_template("correcting.html", parts=table, content=len(table))

	@app.route("/update_amounts")
	def update():
		amounts = request.args.get("input")
		id = request.args.get("checkbox")
		if amounts != None and id != None:
			value1 = f"amounts='{float(amounts.replace(',', '.'))}'"
			value2 = f"id={id}"
			UpdateDatabase(database_parts, table_parts, value1, value2)
		orders = []
		order = [a if a[1] in orders else a for a in
				 FetchDataBase(database_parts, f"SELECT * FROM {table_parts} ORDER BY orders")]
		content = []
		memory = ""
		for a in order:
			if memory == a[1]:
				continue
			else:
				content.append(a)
				memory = a[1]
		return render_template("over_view.html", content=len(content), parts=content)

	@app.route("/order_print")
	def print_order():
		order = request.args.get("Auftragsnummer")
		del_file = request.args.get("checkbox")
		if order != None:
			table = [a if a == order else a for a in FetchDataBase(database_parts, f"SELECT * FROM {table_parts} WHERE orders={order} ORDER BY job ASC")]
			if len(table) >= 1:
				workbook = Workbook()
				sheet = workbook.active
				sheet["A1"] = "ID"
				sheet["B1"] = "Auftragsnummer"
				sheet["C1"] = "Jobnummer"
				sheet["D1"] = "Teilenummer"
				sheet["E1"] = "Menge"
				sheet["F1"] = "Datum"
				for i in range(len(table)):
					sheet[f"A{i+2}"] = table[i][0]
					sheet[f"B{i+2}"] = table[i][1]
					sheet[f"C{i+2}"] = table[i][2]
					sheet[f"D{i+2}"] = table[i][3]
					sheet[f"E{i+2}"] = table[i][4]
					sheet[f"F{i+2}"] = table[i][5]
					print("Excel Liste erzeugt!")
				workbook.save(filename=f"static/OrderPrintLists/Auftrag-{order}.xlsx")
		folder = os.listdir("../pythonProject/static/OrderPrintLists/")
		lists = []
		for file in folder:
			if ".xlsx" in file:
				lists.append(file)
		path = []
		for item in lists:
			path.append(f"static/OrderPrintLists/{item}")
		if del_file != None:
			os.remove(f"../pythonProject/static/OrderPrintLists/{del_file}")
			print(f"Die Datei {del_file} wurde entfernt!")
		return render_template("print_order.html", listen=lists, path=path, content=len(lists))

	@app.route('/order_print')
	def download_file():
		paths = []
		folder = os.listdir("../pythonProject/static/OrderPrintLists/")
		lists = []
		for file in folder:
			if ".xlsx" in file:
				lists.append(file)
		for item in lists:
			paths.append(f"static/OrderPrintLists/{item}")
		path_to = []
		for path in paths:
			path_to.append(path)
		return send_file(path_to,  as_attachment=True)

	@app.route("/download")
	def getPlotCSV():
		download_file = request.args.get("name")
		print(download_file)
		file = f'../pythonProject/static/OrderPrintLists/{download_file}'
		return send_file(file, mimetype='text/csv', attachment_filename=download_file, as_attachment=True)

	@app.route("/part_info")
	def partInfo():
		part_number = request.args.get("Teilenummer")
		if part_number != None:
			part = part_number
			table = [a if a == order else a for a in
					 FetchDataBase(database_part_info, f"SELECT * FROM {table_part_info} WHERE part='{part}'")]
			if len(table) < 1:
				message = (f'Teil "{part}" nicht in Datenbank enthalten! Bzw. Schreibweis überprüfen')
				return render_template("error.html", message=message)
			return render_template("info.html", part=table[0])
		return render_template("partInfo.html")

	@app.route("/part_order")
	def partorder():
		return render_template("partorder.html")

	@app.route("/part_ordered")
	def partsordered():
		date_now = date()
		part_nr = request.args.get("Teilenummer")
		box = request.args.get("Ort")
		amount = request.args.get("Menge")
		ordered = request.args.getlist("Bestellt")
		receive = request.args.getlist("Empfangen")
		if part_nr != None and box != None and amount != None:
			ordered = 0
			receive = 0
			value = f"'{part_nr}', '{box}', {amount}, {ordered}, {receive}, '{date_now}'"
			InsertData( database_part_order, table_order, value)
			ordered = None
			receive = None
		if ordered != None or receive != None:
			if len(ordered) >= 1:
				for check in ordered:
					value1 = f"ordered='checked'"
					value2 = f"id={check}"
					UpdateDatabase(database_part_order, table_order, value1, value2)
			if len(receive) >= 1:
				for check in receive:
					value1 = f"receive='checked'"
					value2 = f"id={check}"
					UpdateDatabase(database_part_order, table_order, value1, value2)
		table = [a if a == order else a for a in FetchDataBase(database_part_order, f"SELECT * FROM {table_order}")]
		return render_template("partordered.html", parts=table, content=len(table))

	@app.route('/order_delete')
	def order_delete():
		orders = []
		orders = [print(a[1]) if a[1] in orders else a for a in FetchDataBase(database_part_order, f"SELECT * FROM {table_order} ORDER BY id")]
		parts = [print(a[1]) if a[1] in orders else a for a in FetchDataBase(database_part_order, f"SELECT * FROM {table_order} ORDER BY id")]
		for a in parts:
			print(a)
		checkbox = request.args.getlist("checkbox")
		print(checkbox)
		if checkbox != None and len(checkbox) > 0:
			print(checkbox[0])
		for box in checkbox:
			print(box[0])
			DeleteFromDatabase(database_part_order, table_order, box)
		return render_template("order_delete.html", content=len(parts), parts=parts)


	if __name__ == "__main__":
		app.run(host=f"{IpReader()}", debug=True)


except FileNotFoundError as error:
	print(f"Fehler 1234 {error}")
	sendMail("ilmarinenerdmann@freenet.de", "Es ist ein Fehler aufgetreten", "Fehler", f"Es ist ein Fehler aufgetreten: {error}")

