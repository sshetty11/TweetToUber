from tweepy.streaming import StreamListener
from FindTweets.keys import Twt_Keys
import json
import sys
import os
import django
import requests
#from twython import Twython
from tweepy import Stream
from geopy.geocoders import Nominatim
from tweepy import OAuthHandler
sys.path.append("c:/Users/Shilpa/TweetToUber")
os.environ["DJANGO_SETTINGS_MODULE"] = "TweetToUber.settings"
django.setup()
from FindTweets.models import User, Request
#classes Start
class listener(StreamListener):
    def on_data(self,data):
        final=json.dumps((data),sort_keys=True,indent=4)
        j=json.loads(final)
        k=json.loads(j)
        location_attributes= None 
        username=k["user"]["screen_name"]
        if k["place"]:
            if k["place"]["bounding_box"]:
                if k["place"]["bounding_box"]["coordinates"]:
                    location_attributes=k["place"]["bounding_box"]["coordinates"]
        ride_request(username,location_attributes)
    def on_error(self,status):
        print status
        
class TweepyClass:
    key_value=Twt_Keys
    CONSUMER_KEY=key_value.CONSUMER_KEY
    CONSUMER_SECRET=key_value.CONSUMER_SECRET
    ATOKEN=key_value.ATOKEN
    ASECRET=key_value.ASECRET
#Classes End1
    
def twtapi():
    twe_attributes=TweepyClass
    auth=OAuthHandler(twe_attributes.CONSUMER_KEY,twe_attributes.CONSUMER_SECRET)
    auth.set_access_token(twe_attributes.ATOKEN,twe_attributes.ASECRET)
    twitterStream=Stream(auth,listener())
    twitterStream.filter(track=['#UberCarRequest'])

#function to send ride request for the user when user tweets step 3
def ride_request(username,location_attributes):
    u=User.objects.get(user_name=username)
    if u:
        url= 'https://sandbox-api.uber.com/v1/requests'
        if location_attributes:
            start_longitude=(location_attributes[0][0][0]+location_attributes[0][1][0]+location_attributes[0][2][0]+location_attributes[0][3][0])/4
            start_latitude=(location_attributes[0][0][1]+location_attributes[0][1][1]+location_attributes[0][2][1]+location_attributes[0][3][1])/4
        else:
            start_latitude,start_longitude=location_converter(u.address)
        response = requests.post(
        url,
        headers={
            'Authorization': 'Bearer %s' % u.access_token,
            'Content-Type':'application/json',
            'Scope':'request'
        },
        data=json.dumps({
            "start_latitude":start_latitude,
            "start_longitude":start_longitude
        }),
        )
        data = response.json()
        result=json.dumps((data),sort_keys=True,indent=4)
        data=json.loads(result)
        #add the status and the request id to the database
        r=Request(user_id=u.id,request_id=data['request_id'],status=data['status'])
        r.save()
        

#convert the address to latitude,longitude
def location_converter(address):
    geolocator=Nominatim()
    location=geolocator.geocode(address)
    return location.latitude, location.longitude

twtapi()
