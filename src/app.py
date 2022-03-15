"""
Author: Kyle Mabry
Main app that runs our application
Copyright 2022
"""
import json
from model import getPrediction
from get_email_contents import getEmailContents
from flask import Flask, request, make_response, render_template
from werkzeug.utils import secure_filename

# Start an instance of Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "../data/emails/"

@app.route('/predict/', methods=['GET', 'POST'])
def predict():

    # Save the email to the emails directory and get a prediction
    email = request.files['email']
    email.save(app.config["UPLOAD_FOLDER"] + secure_filename(email.filename))
    email_body = getEmailContents(email.filename)
    prediction = getPrediction(email_body)

    # Generate the response in json formatY (not currently being used)
    response = make_response(
        json.dumps({"Results": [
            {"Email Topic Prediction:": prediction}
        ]}),
        500,
    )

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)


