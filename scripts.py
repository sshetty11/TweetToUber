#import sys
import time
import os
import django
import sys
import requests
import json
from FindTweets.keys import twilio_keys
sys.path.append("c:/Users/Shilpa/TweetToUber")
os.environ["DJANGO_SETTINGS_MODULE"] = "TweetToUber.settings"
django.setup()
from FindTweets.models import User, Request
from twilio.rest import TwilioRestClient

#Verify if the request is accepted for all the processing requests in the db
def poll_request():
    r=Request.objects.exclude(status='completed')
    for item in r: 
        url = 'https://sandbox-api.uber.com/v1/requests/'+item.request_id
        u=User.objects.get(id=item.user_id)
        #print u.access_token,u.phone_no
        response = requests.get(
        url,
        headers={
            'Authorization': 'Bearer %s' % u.access_token
        }
        )
        data = response.json()
        result=json.dumps((data),sort_keys=True,indent=4)
        j=json.loads(result)
        #print u.phone_no
        if item.status<>j['status']:
            #update the modified request status in the db
            item.status=j['status']
            item.save()
            if j['status']=="accepted" or j['status']=="arriving":
                #print "hi",u.phone_no
                phone_no=u.phone_no
                if j['status']=="accepted":
                    msg_body="Your ride is booked and will be arriving shortly"
                elif j['status']=="arriving":
                    msg_body="Your ride has arrived"
                call_twilio(phone_no,msg_body)
        
    time.sleep(10)
        
def call_twilio(phone_no,msg_body):
    twlkey=twilio_keys
    account_sid=twlkey.ACCOUNT_SID
    auth_token=twlkey.AUTH_TOKEN
    client=TwilioRestClient(account_sid,auth_token)
    message=client.messages.create(body=msg_body,to=phone_no,from_=14088161248)
    #print message.sid


while True:
    poll_request()
    






