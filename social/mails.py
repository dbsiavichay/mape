# -*- coding: utf-8 -*-
import smtplib, codecs
from email.mime.text import MIMEText
from django.conf import settings


def send_mail(to, subject, message):
	HOST=getattr(settings, 'EMAIL_HOST', None)
	PORT=getattr(settings, 'EMAIL_PORT', None)
	USER=getattr(settings, 'EMAIL_HOST_USER', None)
	PASSWORD=getattr(settings, 'EMAIL_HOST_PASSWORD', None)	

	message = MIMEText(message,'plain', 'utf-8')	
	message['Subject'] = subject
	message['From'] = 'Mape'
	message['To'] = to

	server = smtplib.SMTP(HOST, PORT)
	server.starttls()
	server.login(USER, PASSWORD)
	 	
	server.sendmail(message['From'], message['To'], message.as_string())
	server.quit()

def send_activate_account(user):
	from django.urls import reverse
	link = 'http://localhost:8000' + reverse('activate_account', args=[str(user)])

	message = """
		Activa tu cuenta.

		Solo te queda un ultimo paso, activa tu cuenta presionando el enlace que esta en la parte de abajo.
		
		Enlace: %s		
		""" % link

	send_mail(user.email, 'Activa tu cuenta', message)
