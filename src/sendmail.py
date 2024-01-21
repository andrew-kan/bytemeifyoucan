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
    reply["To"] = original["Reply-To"] or original["From"]
    reply["Subject"] = "Re: " + original["Subject"]
    reply["In_Reply-To"] = original["Message-Id"]
    reply["References"] = (original["References"] or "") + " " + original["Message-Id"]
    reply.set_content("This is the reply text.")

    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
        smtp.login(email_account, email_password)
        smtp.send_message(reply)
    print("Reply sent!")

