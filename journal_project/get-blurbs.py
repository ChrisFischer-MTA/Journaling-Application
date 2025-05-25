# Chris Fischer
# Support Script for the jornaling app - should get the outstanding messages
# from the signal API and create unlinked blurb objects
import requests
import json
import sys
import os
import time

def process_blurb(incoming_message):
    # Get user object
    user_object = User.objects.all().filter(username=f'{WEBAPP_USERNAME}')[0]
    print(incoming_message)
    print(user_object)
    temp = Blurb.objects.create(blurb_text=incoming_message, user=user_object)
    temp.save()

# First thing - let's grab the phone number
# This is treated as a secret
SIGNAL_NUMBER = os.environ.get("SIGNAL_NUMBER")

# There is an edge case where we execute this script via cron and it doesn't load enviroment variables
# So, as a result, we have to account for that.
# Google says I could use the dotenv library, but, easy enough to just load it by hand
if SIGNAL_NUMBER is None:
    with open('/etc/enviroment', 'r') as ifp:
        lines = ifp.read().splitlines()
        for line in lines:
            os.environ[line.split('=')[0]] = line.split('=')[1]

# Now that we know our enviroment variables are set, let's load in whatever else we need.
SIGNAL_NUMBER = os.environ.get("SIGNAL_NUMBER")
WEBAPP_USERNAME = os.environ.get("WEBAPP_USERNAME")



# This is some special syntatical suger that I learned a few years back.
# We first add out list of django apps to our path. For this, we only really
# need journalmain but adding journal_project is just good hygene
# sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "journal_project.settings")

# Set up the django enviroment for us to interact with
from django.core.wsgi import get_wsgi_application
get_wsgi_application()

# Now, we import models
from journalmain.models import Blurb
from django.contrib.auth.models import User



headers = {
    'Content-Type': 'application/json',
}

# We double up on brackets to escape them for the curly braces
data = f'{{"number": {SIGNAL_NUMBER}}}'

response = requests.get(f'http://signal-api:8080/v1/receive/{SIGNAL_NUMBER}', headers=headers, data=data)
for message in response.json():
    if(message.get("envelope") is not None):
        if(message["envelope"].get("dataMessage") is not None):
            if(message["envelope"]["dataMessage"].get("message")) is not None:
                process_blurb(message["envelope"]["dataMessage"]["message"])


