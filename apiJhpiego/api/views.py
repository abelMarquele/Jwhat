
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from apiJhpiego.api.serializers import UserSerializer, GroupSerializer
from django.shortcuts import render



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



import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt



from django.conf import settings
import os
import requests
from decouple import config

WHATSAPP_URL = 'https://graph.facebook.com/v16.0/103297242770340/messages'
def sendWhatsAppMessage(phoneNumber, message):
    token = config('WHATSAPP_TOKEN', default='')

    if not token:
        return "Erro: Token de acesso não encontrado."

    headers = {"Authorization": token}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_URL, headers=headers, json=payload)
    if response.status_code == 200:
        ans = response.json()
        return ans
    else:
        return "Erro ao enviar mensagem: " + response.text


# Exemplo de uso:
# phoneNumber = "258844680366"
# message = "Olá! Esta é uma mensagem de teste."
# result = sendWhatsAppMessage(phoneNumber, message)
# print(result)


@csrf_exempt
def whatsappWebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = 'whatsapp-webhook'
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else: 
            return HttpResponse('error', status=403)
 
        
    if request.method == "POST":
        data = json.loads(request.body)

        if 'object' in data and 'entry' in data:
            # print('33. dentro do if')
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                        phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                        profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        fromId = entry['changes'][0]['value']['messages'][0]['from']
                        messageId = entry['changes'][0]['value']['messages'][0]['id']
                        timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        phoneNumber = "258844680366"
                        message = 'RE: {} was received'.format(text)
                        sendWhatsAppMessage(phoneNumber, message)
                        print('66. sendWhatsAppMessage(phoneNumber, message)',sendWhatsAppMessage(phoneNumber, message))
                except:
                    pass
        # print('77. fora de if')
        return HttpResponse('success', status=200)
