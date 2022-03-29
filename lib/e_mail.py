import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def sendMail1(MailText):
	senderEmail = "sender_Mail_Adresse"
	empfangsEmail = "empfänger_Mail_Adresse"
	msg = MIMEMultipart()
	msg['From'] = senderEmail
	msg['To'] = empfangsEmail
	msg['Subject'] = "Neustart RaspberryPi"

	emailText = MailText
	msg.attach(MIMEText(emailText, 'html'))
	attachment = "pfad zu der angehängeten Datei"
	server = smtplib.SMTP('smtp_des_Servers', "port_des_servers") # Die Server Daten
	server.starttls()
	server.login(senderEmail, "Passwort") # Das Passwort
	text = msg.as_string()
	server.sendmail(senderEmail, empfangsEmail, text,)
	server.quit()
	print("Mail versendet")

def sendMail(mailTo, subject,  title, MailText):
	to = str(mailTo)
	print("Starte versenden der Mail")
	gmail__user = 'sender_Mail_adresse'
	hanse_franz_user = 'empfänger_Mail_Adresse'
	gmail__pwd = 'sender_passwort'
	hanse_franz_pwd = 'sender_passwort2'
	smtp_gmail = "sender_smtp"
	port_gmail = "sender_port"
	smtp_hanse_franz = "sender_smtp"
	port_hanse_franz = "sender_port"
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
