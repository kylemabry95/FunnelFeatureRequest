"""
Author: Kyle Mabry
Model that is trained on email data.
Copyright 2022
"""
import os
import warnings
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
from keras.layers.embeddings import Embedding
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
from get_email_contents import getEmailContents

DATA_DIRECTORY = "../data/emails"

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
print(all_email_bodies.shape)

# Split the data into training and testing data
bodies_train, bodies_test, headers_train, headers_test = train_test_split(all_email_bodies, all_email_headers, test_size=0.3, random_state=43)

# Define the model
body_size = 11313
header_size = 32
maxlen = 11313

model = Sequential()
model.add(Embedding(input_dim=body_size, output_dim=header_size, input_length = maxlen))
model.add(SimpleRNN(header_size, return_sequences=True))
model.add(Dropout(0.2))
model.add(SimpleRNN(header_size, return_sequences=True))
model.add(Dropout(0.2))
model.add(SimpleRNN(header_size))
model.add(Dense(2, activation='softmax'))
model.compile(loss = 'binary_crossentropy', optimizer='adam', metrics = ['accuracy'])
warnings.filterwarnings("ignore")
model.summary()

# fit the model to the training set
run_information = model.fit(bodies_train, headers_train, epochs=10, validation_split=0.3)

# Evaluate the model
scores = model.evaluate(bodies_test, headers_test)
print("Accuracy: %.2f%%" % (scores[1] * 100))
warnings.filterwarnings("ignore")



