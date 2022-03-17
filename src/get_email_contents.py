"""
Author: Kyle Mabry
Gets the body from an email text file.
Copyright 2022
"""
import os
import email
from email.parser import BytesParser
from email.policy import default
import numpy as np
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer

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


def get_all_emails():
    """Gets all emails in the DATA_DIRECTORY."""

    # Get all email data
    all_email_headers = []
    all_email_bodies = []
    for (root, dirs, files) in os.walk(DATA_DIRECTORY):
        for file in files:
            header, body = getEmailContents(file)
            all_email_headers.append(header)
            all_email_bodies.append(body)

    # convert to np array
    all_email_headers = np.asarray(all_email_headers)
    all_email_bodies = np.asarray(all_email_bodies)

    # Tokenize the input data
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_email_headers)
    tokenizer.fit_on_texts(all_email_bodies)
    word_index = tokenizer.word_index
    print("found", len(word_index), "words.")

    sequences_headers = tokenizer.texts_to_sequences(all_email_headers)
    sequences_bodies = tokenizer.texts_to_sequences(all_email_bodies)

    maxlen_header = 100
    maxlen_body = 500
    all_email_headers = pad_sequences(sequences_headers, maxlen=maxlen_header)
    all_email_bodies = pad_sequences(sequences_bodies, maxlen=maxlen_body)

    print("Shape of headers:", all_email_headers.shape)
    print("Shape of body:", all_email_bodies.shape)

    return all_email_headers, all_email_bodies


if __name__=="__main__":
    getEmailContents("00002")