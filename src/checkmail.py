import imaplib
from email.header import decode_header
import os
import email
import sys
from time import sleep
from celery_config import create_celery_app
app = create_celery_app(None)
# Import tasks
import tasks

refresh_delay = 20
email_account = "bytemetest69@gmail.com"
email_password = "jxgmdufkfjmxaeie"
imap_server = "imap.gmail.com"
    
def process_email(data):
    msg = email.message_from_bytes(data[0][1])
    content = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            content.append(part.get_payload(decode=True))
    msg_json = {
        "Message-ID": msg["Message-ID"],
        "Date": msg["Date"],
        "Content-Type": msg["Content-Type"],
        "Subject": msg["Subject"],
        "From": msg["From"],
        "Reply-To": msg["Reply-To"],
        "To": msg["To"],
        "Content": content
    }
    tasks.process_email.delay(msg_json)

def check_mail(conn):
    print("Checking for new messages...")
    conn.select("INBOX", readonly=False)
    (retcode, messages) = conn.search(None, '(UNSEEN)')
    if retcode == 'OK':
        if messages[0] == b'':
            print("No new messages.")
        else:
            for num in messages[0].decode("utf-8").split(' '):
                # print('Processing : #', num)
                typ, data = conn.fetch(num,'(RFC822)')
                process_email(data)
                typ, data = conn.store(num,'+FLAGS','\\Seen')
            print("Finished fetching new messages.")
    conn.close()

def fetching_loop():
    print("CHECKING MAIL :)")
    conn = imaplib.IMAP4_SSL(imap_server)
    conn.login(email_account, email_password)

    try:
        while True:
            check_mail(conn)
            sleep(refresh_delay)
    finally:
        conn.close()

fetching_loop()