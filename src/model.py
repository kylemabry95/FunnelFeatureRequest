"""
Author: Kyle Mabry
Creates a model that can determine the topic of an email given the email's body.
Copyright 2022
"""

import openai

# I'm trusting you with this ;)
openai.api_key = "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"


def getPrediction(email_body):
    """Gets a subject prediction when given an email's contents"""

    response = openai.Completion.create(
      engine="davinci-instruct-beta",
      prompt="Determine the topic of the following email:\n\"\"\"\"\"\"\n%s\n\"\"\"\"\"\"\n" % email_body,
      temperature=0.5,
      max_tokens=216,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\"\"\"\"\"\""]
    )

    text_response = response.choices[0].text
    print("\nEmail Topic:\n" + text_response + "\n")

    return text_response

