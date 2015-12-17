from tweepy.streaming import StreamListener
from FindTweets.keys import Keys
import json
#classes Start
class listener(StreamListener):
    def on_data(self,data):
        final=json.dumps((data),sort_keys=True,indent=4)
        j=json.loads(final)
        k=json.loads(j)
        if k["place"]:
            if k["place"]["bounding_box"]:
                if k["place"]["bounding_box"]["coordinates"]:
                    print k["place"]["bounding_box"]["coordinates"]
             
        '''for kI in j.split(","):
            p=kI.split(":")
            #print p
            if p[0]==u'"coordinates"':
               #print p
               if  p[1]!=u'null':
                   print j'''
        #print j
    def on_error(self,status):
        print status
class TweepyClass:
    #def __init__(self,consumer_key,consumer_secret,atoken,asecret):
    key_value=Keys
    CONSUMER_KEY=key_value.CONSUMER_KEY
    CONSUMER_SECRET=key_value.CONSUMER_SECRET
    ATOKEN=key_value.ATOKEN
    ASECRET=key_value.ASECRET
#Classes End1
