"""
Author: Kyle Mabry
Model that is trained on email data.
Copyright 2022
"""
import warnings
import numpy as np
from keras.constraints import maxnorm
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Dropout, Embedding
from sklearn.model_selection import train_test_split
from get_email_contents import get_all_emails


def create_RNN(hidden_units, dense_units, input_shape, activation):
    """Creates the model skeleton"""
    model = Sequential()
    model.add(Embedding(input_dim=149056, output_dim=32, input_length=hidden_units))
    model.add(SimpleRNN(hidden_units, return_sequences=True, input_shape=input_shape, activation=activation[0]))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(hidden_units, return_sequences=True, input_shape=input_shape, activation=activation[0]))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(hidden_units,input_shape=input_shape, activation=activation[0]))
    model.add(Dense(units=dense_units, activation=activation[1]))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.summary()
    return model


# Get the emails from the "database"
all_email_headers, all_email_bodies = get_all_emails()
all_email_headers = np.reshape(all_email_headers, (all_email_headers.shape[0], all_email_headers.shape[1], 1))
all_email_bodies = np.reshape(all_email_bodies, (all_email_bodies.shape[0], all_email_bodies.shape[1], 1))

# Split the data into training and testing data
bodies_train, bodies_test, headers_train, headers_test = train_test_split(all_email_bodies, all_email_headers, test_size=0.3, random_state=43)
print("bodies:", bodies_train.shape)
print("headers:", headers_train.shape)

# Define the model
body_size = len(bodies_train)
maxlen = 500

# fit the model to the training set
our_model = create_RNN(maxlen, 100, (maxlen,1), activation=['linear', 'linear'])
run_information = our_model.fit(bodies_train, headers_train, epochs=10, validation_split=0.3)

# Evaluate the model
scores = our_model.evaluate(bodies_test, headers_test)
print("Accuracy: %.2f%%" % (scores[1] * 100))
warnings.filterwarnings("ignore")

