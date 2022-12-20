from django.shortcuts import render
import os
import time
import json
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .agora_key.RtcTokenBuilder import RtcTokenBuilder
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import random

from .models import RoomMember


def getToken(request):
    appId = settings.AGORA_APP_ID
    print(appId)
    appCertificate = settings.AGORA_APP_CERTIFICATE
    channelName = request.GET.get('channel')
    uid =  random.randint(1,230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse ({'token':token, 'uid':uid}, safe=False)


def videochatlobbyviews(request):
    return render(request, 'videochat/videochatlobby.html')


def videochatroomviews(request):
    return render(request, 'videochat/videochatroom.html')

# View to initiate a direct videochat session with current user information.
# The initiator of a direct videochat will always be set to the videouser1 field of each Private VideoChat Room object.
# If the current user == user2 of the object they will access that existing room.
def getToken(request):
    appId = '03dd86e8444b4b8b98cd6b963c9b3a96'
    appCertificate = '5ade5ddf4cc944cab94803737ab5d637'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)