import smtplib

def emailMe(emailBody):

    login_username = 'msi.pc.christian@gmail.com'
    login_password = '0836550600'

    from_email = 'msi.pc.christian@gmail.com'
    to_email = 'cjluus@gmail.com'

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(login_username, login_password)

    smtpObj.sendmail(from_email, to_email, 'Subject: Shopping List\n' + emailBody)

    smtpObj.quit()