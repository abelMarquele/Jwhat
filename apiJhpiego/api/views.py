
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from apiJhpiego.api.serializers import UserSerializer, GroupSerializer
from django.shortcuts import render

from .functions import *
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def home(request):
    return render(request, 'index.html',{})



@csrf_exempt
def whatsappWebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = 'whatsapp-webhook'
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else: 
            return HttpResponse('error', status=403)
 
        
    if request.method == "POST":
        data = json.loads(request.body)

        return HttpResponse('success', status=200)
        