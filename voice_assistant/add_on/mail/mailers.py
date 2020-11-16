# -*- coding: utf-8 -*-

import smtplib

gEmailSender, gEmailPassword, gEmailRecipients = get_credentials()

mailer = smtplib.SMTP('smtp.gmail.com', 587)
# http://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems

mailer.ehlo()
mailer.starttls()
mailer.ehlo()
mailer.login(gEmailSender, gEmailPassword)
# mailer.sendmail(gEmailSender, gEmailRecipients, 'test pixelmatic')
mailer.quit()

sender = 'from@fromdomain.com'
receivers = ['rama.ahn@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
    print("Successfully sent email")
except SMTPException as e:
    print(f"Error: unable to send email \n{e}")
