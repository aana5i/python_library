import smtplib
from config.config import get_credentials


gEmailSender, gEmailPassword, gEmailRecipients = get_credentials()

mailer = smtplib.SMTP('smtp.gmail.com', 587)
# http://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems

mailer.ehlo()
mailer.starttls()
mailer.ehlo()
mailer.login(gEmailSender, gEmailPassword)
# mailer.sendmail(gEmailSender, gEmailRecipients, 'test pixelmatic')
mailer.quit()
