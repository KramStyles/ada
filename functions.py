import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from passlib.hash import sun_md5_crypt as Sun


def checkEmpty(shadow):
    empty = False
    for case in shadow:
        if not case:
            empty = True
    return empty


def password(word):
    return Sun.encrypt(word)

def emailSender(send_to="authcourse67@gmail.com", Subject="Mail from Our App", Message="Default message been sent!"):
    mail = 'authcourse67@gmail.com'
    password = '@auth2020'
    subject = Subject
    message = Message

    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # Secure using SSL

    server.login(mail, password)
    text = msg.as_string()

    try:
        server.sendmail(mail, send_to, text)
        msg = 'ok'
    except Exception as err:
        msg = f"Error: {err}"
    return msg