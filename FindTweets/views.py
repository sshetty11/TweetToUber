from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from rauth import OAuth2Service
from FindTweets.keys import Uber_keys
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
    template = loader.get_template('FindTweets/index.html')
    context = RequestContext(request)
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
    return render(request,'FindTweets/index.html',{})

#VIEW END

    

#REGISTERING PART START
#function to register the user  step 1
def login_redirect():
    keys=Uber_keys
    uber_api = OAuth2Service(
     client_id=keys.CLIENT_ID,
     client_secret=keys.CLIENT_SECRET,
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
    keys=Uber_keys
    parameters = {
        'redirect_uri': 'http://localhost:8000/FindTweets/cburl',
        'code': request.GET.get('code'),
        'grant_type': 'authorization_code',
    }

    response = requests.post(
    'https://login.uber.com/oauth/token',
    auth=(
        keys.CLIENT_ID,
        keys.CLIENT_SECRET,
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
    return render(request,'FindTweets/index.html',{'hashvalue':'User Registered successfully'})

#REGISTERING PART END

