import os,smtplib 
import email.mime.text

emsg = 'The contents of this test email is the following' 
me = 'ben.buckey@icloud.com'
you = 'ben.buckey@icloud.com' 

if __name__ == '__main__':
	msg = email.mime.text.MIMEText(emsg)
	msg['Subject'] = 'The contents of this test email is the following' 
	msg['From'] = me
	msg['To'] = you

	s = smtplib.SMTP('localhost',465)
	s.sendmail(msg['From'] , msg['To'], msg.as_string() )
	s.quit()

