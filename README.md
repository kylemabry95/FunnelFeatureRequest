## Funnel Feature Request
Author: [Kyle Mabry](https://github.com/kylemabry95)

### Prerequisites
- Python >= 3.10.0

### Getting Started
First, create a new conda environment and install the dependencies using the `environment.yml` file:
```shell
conda env create -f environment.yml
```
Request the API key for OpenAI from me at kmabry[aT]bu[doT]edu and place this in the `src/model.py` file.

Next navigate to src and run app.py

Send a post request using PostMan to the IP address provided by Flask at the /predict/ route.
The Post request should be in the form of "form-data" where the key is "email" and it accpets a 
file which is the contents of the email.

This application doesn't re-invent the wheel, so-to-speak, but instead relies on the Semantic 
Completion API provided by OpenAI.

See the LICENSE file for copyright questions.

