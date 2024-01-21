import smtplib
import email
from email.header import decode_header
from email.message import EmailMessage
from email.mime.text import MIMEText

email_account = "bytemetest69@gmail.com"
email_password = "jxgmdufkfjmxaeie"
smtp_server = "smtp.gmail.com"
from_address = "Byteme Test <bytemetest69@gmail.com>"

def send_email(subject, body, recipient):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_account
    msg['To'] = recipient
    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
        smtp.login(email_account, email_password)
        smtp.send_message(msg)
    print("Message sent!")

def reply_to_email(original, reply_msg):
    reply = email.message.EmailMessage()
    original["Message-ID"] = original["Message-ID"].replace("\r\n ", "")
    reply["From"] = from_address
    reply["To"] = original["Reply-To"] or original["From"]
    reply["Subject"] = "Re: " + original["Subject"]
    reply["In-Reply-To"] = original["Message-ID"]
    reply["References"] = original["Message-ID"]
    reply.set_content(reply_msg)

    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
        smtp.login(email_account, email_password)
        smtp.send_message(reply)
    print("Reply sent!")
