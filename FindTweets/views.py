from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from twython import Twython
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from FindTweets.models import User
from FindTweets.envs import TweepyClass,listener
import json
# Create your views here.
def index(request):
    hashvalue='A'
    User.objects.all()
    if request.method=='POST':
        hashvalue=request.POST.get('hashtag')
        twtapi()
    template = loader.get_template('FindTweets/index.html')
    context = RequestContext(request, {
    'hashvalue':  hashvalue,
    })
    return HttpResponse(template.render(context))


#Function      
def twtapi():
    twe_attributes=TweepyClass
    auth=OAuthHandler(twe_attributes.CONSUMER_KEY,twe_attributes.CONSUMER_SECRET)
    auth.set_access_token(twe_attributes.ATOKEN,twe_attributes.ASECRET)
    twitterStream=Stream(auth,listener())
    twitterStream.filter(track=['Uber'])
    #twitter=Twython(APP_KEY,APP_SECRET,oauth_version=2)
    
    #ACCESS_TOKEN=twitter.obtain_access_token()
    #twitter=Twython(APP_KEY,access_token=ACCESS_TOKEN)
    #results=twitter.search(q='abcdefghij')
    #final= json.dumps((results),sort_keys=True,indent=4)
    #j=json.loads(final)
    #for i in range(0,len(j['statuses'])):
     #   print "TWEET:"
     #   k=j['statuses'][i]['text'].encode('ascii','ignore')
     #   print k
    #print j['statuses'][0]['text']
    #return results
