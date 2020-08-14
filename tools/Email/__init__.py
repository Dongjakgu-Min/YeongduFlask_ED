import smtplib
import os

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login(os.environ['MAIL_ID'], os.environ['MAIL_PW'])
