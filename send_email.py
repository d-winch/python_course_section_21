from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email = "winchheightcollector@gmail.com"
    from_password = "__REDACTED__"
    to_email = email
    subject = "Height Data"
    body = "Your height is <strong>%s</strong>. Average height of <strong>%s</strong> people is <strong>%s</strong>." % (height, count, average_height)

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    gmail.send_message(msg)
