import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def sendMail1(MailText):
	senderEmail = "u42570@hanse-franz.de"
	empfangsEmail = "ilmarinenerdmann@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = senderEmail
	msg['To'] = empfangsEmail
	msg['Subject'] = "Neustart RaspberryPi"

	emailText = MailText
	msg.attach(MIMEText(emailText, 'html'))
	attachment = "/../pythonProject/static/OrderPrintLists/Auftra-6902773.xlsx"
	server = smtplib.SMTP('mail.manitu.de', 993) # Die Server Daten
	server.starttls()
	server.login(senderEmail, "KRYudQXhZKPM") # Das Passwort
	text = msg.as_string()
	server.sendmail(senderEmail, empfangsEmail, text,)
	server.quit()
	print("Mail versendet")

def sendMail(mailTo, subject,  title, MailText):
	to = str(mailTo)
	print("Starte versenden der Mail")
	gmail__user = 'ilmarinenerdmann@googlemail.com'
	hanse_franz_user = 'u42570@hanse-franz.de'
	gmail__pwd = 'nmqiueatzwcjveay'
	hanse_franz_pwd = 'KRYudQXhZKPM'
	smtp_gmail = "smtp.gmail.com"
	port_gmail = 587
	smtp_hanse_franz = "mail.manitu.de"
	port_hanse_franz = 993
	smtpserver = smtplib.SMTP(smtp_gmail, port_gmail)
	smtpserver.ehlo()
	print("Mailserver verbindungs aufbau")
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail__user, gmail__pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail__user + '\n' 'Subject:' + subject + '\n' + f'{title} \n'
	print(title)
	msg = header + f'\n {MailText} \n\n'
	smtpserver.sendmail(gmail__user, to, msg)
	smtpserver.close()
	print("Mail versendet")
