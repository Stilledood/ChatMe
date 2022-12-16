from django.shortcuts import render
import os
import time
import json
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .agora_key.RtcTokenBuilder import RtcTokenBuilder,Role_Attendee
from  pusher import Pusher

#Instantiate a pusher client
pusher_client = Pusher(app_id=os.environ.get('PUSHER_APP_ID'),
                key=os.environ.get('PUSHER_KEY'),
                secret=os.environ.get('PUSHER_SECRET'),
                ssl=True,
                cluster=os.environ.get('PUSHER_CLUSTER'))

@login_required(login_url='dj-auth:login')
def index(request):
    User = get_user_model()
    all_users = User.objects.filter(id=request.user.id).only('id','username')
    return render(request,'videochat/index.html',context={'all_users':all_users})

def pusher_auth(request):
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.post['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id':request.user.id,
                'name': request.user.username
            }
        }
    )
    return  JsonResponse(payload)

def generate_token(request):
    appID = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    channelName = json.loads(request.body.decode('utf-8'))['channelName']
    userAccount = request.user.username
    expiraTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expiraTimeInSeconds
    token = RtcTokenBuilder.buildTokenWithAccount(appId=appID, appCertificate=appCertificate, channelName=channelName, account=userAccount, Role_Attendee, privilegeExpiredTs=privilegeExpiredTs)
    return JsonResponse({'token':token, 'appID':appID})


def call_user(request):
    body = json.loads(request.body.decode('utf-8'))
    user_to_call = body['user_to_call']
    caller = request.user.id
    channel_name = body['channel_name']

    pusher_client.trigger(
        'presence-online-channel',
        'make-agora-call',
        {
            'userToCall': user_to_call,
            'channelName': channel_name,
            'from': caller
        },
    )
    return JsonResponse({'message':'call has been placed'})

