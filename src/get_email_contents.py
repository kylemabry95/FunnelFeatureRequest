"""
Author: Kyle Mabry
Gets the body from an email text file.
Copyright 2022
"""
import os
import email
from email.parser import BytesParser
from email.policy import default

DATA_DIRECTORY = "../data/emails"


def getEmailContents(email_path):
    """Given a single email this function returns the body of the email as text"""

    email_file = open(os.path.join(DATA_DIRECTORY, email_path))
    try:
        message = email.message_from_file(email_file)
    except UnicodeDecodeError:
        return "null", "null"

    # Get email subject
    with open(os.path.join(DATA_DIRECTORY, email_path), 'rb') as fp:
        msg = BytesParser(policy=default).parse(fp)
        email_subject = msg["Subject"]

    b = message
    email_body = "None"
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # skip attachemnts
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                email_body = part.get_payload(decode=True)  # decode
                break
    # if no attachments (in our case there are likely none and this will run)
    else:
        # Get email body
        email_body = str(b.get_payload(decode=True))

    return email_subject, email_body

if __name__=="__main__":
    getEmailContents("00002")