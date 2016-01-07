from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
#from twython import Twython
#from tweepy import Stream
#from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener
#from FindTweets.envs import TweepyClass,listener
from rauth import OAuth2Service
from FindTweets.models import User, Request
from django.views.decorators.csrf import csrf_protect
import json
import requests
first_name=''
username=''
phone=0
user_address=''

#VIEW START
def index(request):
    hashvalue='A'
    template = loader.get_template('FindTweets/index.html')
    context = RequestContext(request)
    #return HttpResponse(template.render(context))
    return render(request,'FindTweets/index.html',{})

#redirected to this view on post
def redirect(request):
    global username
    global phone
    global user_address
    global first_name
    if request.method=='POST':
        if request.POST["action"]=="Register":
            username=request.POST.get('username')
            phone=request.POST.get('phone')
            user_address=request.POST.get('address')
            first_name=request.POST.get('name')
            return login_redirect()
    template = loader.get_template('FindTweets/index.html')
    context = RequestContext(request)
    #return HttpResponse(template.render(context))
    return render(request,'FindTweets/index.html',{})

#VIEW END

    

#REGISTERING PART START
#function to register the user  step 1
def login_redirect():
    uber_api = OAuth2Service(
     client_id='g2qpdEcMsUT59bZ0vp7QNDdaX4l7cx02',
     client_secret='dSuZXHijPe1LaH-xTh1eFOq1ZYnKtWKZzUK5IWQM',
     name='TweetToRide',
     authorize_url='https://login.uber.com/oauth/authorize',
     access_token_url='https://login.uber.com/oauth/token',
     base_url='https://api.uber.com/v1/',
     )
    parameters = {
    'response_type': 'code',
    'redirect_uri': 'http://localhost:8000/FindTweets/cburl',
    'scope': 'profile request',
    }

    # Redirect user here to authorize your application
    login_url = uber_api.get_authorize_url(**parameters)
    #print login_url
    #redirect to uber login url
    return HttpResponseRedirect(login_url)


#callback url used once the user has signed in to the uber login url step 2
def cburl(request):
    # Once your user has signed in using the previous step you should redirect
    # them here
    global username
    global phone
    global first_name
    global user_address
    parameters = {
        'redirect_uri': 'http://localhost:8000/FindTweets/cburl',
        'code': request.GET.get('code'),
        'grant_type': 'authorization_code',
    }

    response = requests.post(
    'https://login.uber.com/oauth/token',
    auth=(
        'g2qpdEcMsUT59bZ0vp7QNDdaX4l7cx02',
        'dSuZXHijPe1LaH-xTh1eFOq1ZYnKtWKZzUK5IWQM',
    ),
    data=parameters,
    )

    # This access_token is what we'll use to make requests in the following
    # steps
    accesstoken = response.json().get('access_token')
    template = loader.get_template('FindTweets/index.html')
    context = RequestContext(request, {
    'hashvalue':"User Registered successfully",
    })
    #save the access token for the user in the db
    print first_name,user_address
    u=User(name=first_name,address=user_address,user_name=username,phone_no=phone,access_token=accesstoken)
    u.save()
    #return HttpResponse(template.render(context))
    return render(request,'FindTweets/index.html',{'hashvalue':'User Registered successfully'})

#REGISTERING PART END

