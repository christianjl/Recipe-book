import smtplib

def emailMe(emailBody):

login_username = 
login_password = 

from_email = 
to_email = 

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('login_username', 'login_password')

    smtpObj.sendmail('from_email', 'to_email', 'Subject: Subject\n' + emailBody)

    smtpObj.quit()