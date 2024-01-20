import imaplib
import smtplib
from email.header import decode_header
from email.message import EmailMessage
from email.mime.text import MIMEText
import webbrowser
import os
import email
import sys
from time import sleep

# account credentials
email_account = "bytemetest69@gmail.com"
email_password = "jxgmdufkfjmxaeie"
imap_server = "imap.gmail.com"
smtp_server = "smtp.gmail.com"

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def process_email(msg):
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            print("Subject:", subject)
            print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        print(body)
                    elif "attachment" in content_disposition:
                        # download attachment
                        filename = part.get_filename()
                        if filename:
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                            open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    print(body)
                    # TODO send this text to chatgpt and get reply

            if content_type == "text/html":
                # if it's HTML, create a new HTML file and open it in browser
                folder_name = clean(subject)
                if not os.path.isdir(folder_name):
                    # make a folder for this email (named after the subject)
                    os.mkdir(folder_name)
                filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                open(filepath, "w").write(body)
                # webbrowser.open(filepath)
            print("="*100)
            reply_to_email(msg, email_account, email_password, smtp_server)

def fetch_email_loop(email_account, email_password, imap_server="imap.gmail.com"):
    conn = imaplib.IMAP4_SSL(imap_server)
    try:
        (retcode, capabilities) = conn.login(email_account, email_password)
    except:
        print(sys.exc_info()[1])
        sys.exit(1)

    while True:
        print("Checking for new messages...")
        conn.select("INBOX")
        (retcode, messages) = conn.search(None, '(UNSEEN)')
        if retcode == 'OK':
            if messages[0] == b'':
                print("No new messages.")
            else:
                for num in messages[0].decode("utf-8").split(' '):
                    print('Processing : #', num)
                    typ, data = conn.fetch(num,'(RFC822)')
                    process_email(data)
                    typ, data = conn.store(num,'+FLAGS','\\Seen')
                    # msg = email.message_from_string(data[0][1].decode("utf-8"))
                    # print(data,'\n',30*'-')
                    # print(msg)
                print("Finished fetching new messages.")
        sleep(10)
    conn.close()

def send_email_from_file(subject, filename, sender_email, sender_password, recipient, smtp_server="smtp.gmail.com"):
    with open(filename) as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient
    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
       smtp.login(sender_email, sender_password)
       smtp.send_message(msg)
    print("Message sent!")

def send_email(subject, body, sender_email, sender_password, recipient, smtp_server="smtp.gmail.com"):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient
    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print("Message sent!")

def reply_to_email(original, sender_email, sender_password, smtp_server="smtp.gmail.com"):
    reply = email.message.EmailMessage()
    reply["To"] = original["Reply-To"] or original["From"]
    reply["Subject"] = "Re: " + original["Subject"]
    reply["In_Reply-To"] = original["Message-Id"]
    reply["References"] = (original["References"] or "") + " " + original["Message-Id"]
    reply.set_content("This is the reply text.")

    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(reply)
    print("Reply sent!")

    # result, data = imap_server.fetch(email_id, "(RFC822)")
    # raw_email = data[0][1]
    # email_message = email.message_from_bytes(raw_email)


subject = "Email Subject"
body = "This is an automated message."
send_email(subject, body, email_account, email_password, email_account, smtp_server)

# fetch_email_loop(email_account, email_password, imap_server)