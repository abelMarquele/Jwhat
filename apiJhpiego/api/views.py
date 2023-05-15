
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


# from .functions import *
# import json
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def whatsappWebhook(request):
#     if request.method == 'GET':
#         VERIFY_TOKEN = 'whatsapp-webhook'
#         # mode = request.GET['hub.mode']
#         mode = request.GET.get('hub.mode')

#         token = request.GET['hub.verify_token']
#         challenge = request.GET['hub.challenge']

#         print('request',request)
#         print('VERIFY_TOKEN',VERIFY_TOKEN)
#         print('',)

#         if mode == 'subscribe' and token == VERIFY_TOKEN:
#             return HttpResponse(challenge, status=200)
#         else: 
#             return HttpResponse('error', status=403)
 
        
#     if request.method == "POST":
#         data = json.loads(request.body)
#         if 'object' in data and 'entry' in data:
#             if data['object'] == 'whatsapp_business_account':
#                 try:
#                     for entry in data['entry']:
#                         phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
#                         phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
#                         profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
#                         whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
#                         fromId = entry['changes'][0]['value']['messages'][0]['from']
#                         messageId = entry['changes'][0]['value']['messages'][0]['id']
#                         timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
#                         text = entry['changes'][0]['value']['messages'][0]['text']['body']

#                         phoneNumber = "258844680366"
#                         message = 'RE: {} was receive'.format(text)
#                         sendWhatsAppMessage(phoneNumber, message)
#                 except:
#                     pass

#         return HttpResponse('success', status=200)
        
# from .functions import *

import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

WHATSAPP_URL = 'https://graph.facebook.com/v16.0/103297242770340/messages'
WHATSAPP_TOKEN = 'Bearer EAACwv64kYI4BAHaWJwUUzZBMA93EAKO4ygH0N6w2FikZBhRfQcpRG10o6ZBBkUGrj6tzInl1Smtfni8XJSvkjaJ8NzDoKZBYaiCAaoZAlPhtslIKfbedwS2SxdumOIi8HxjSkZC5jCwoIosqhsQLp3tLBtvWfGBgr7VfGcoUrc0BRv1flSdTf2RPgbhk7QgtqbipzyECpOZB30oo653VJNP'

def sendWhatsAppMessage(phoneNumber, message):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return "Mensagem enviada com sucesso!"
    else:
        return "Erro ao enviar mensagem: " + response.text


# Exemplo de uso:
phoneNumber = "258844680366"
message = "Olá! Esta é uma mensagem de teste."
result = sendWhatsAppMessage(phoneNumber, message)
print(result)


@csrf_exempt
def whatsappWebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = 'whatsapp-webhook'
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        print('1. request',request)
        print('2. VERIFY_TOKEN',VERIFY_TOKEN)
        print('3. mode',mode)
        print('4. token',token)
        print('5. challenge',challenge)

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('6. token validado')
            return HttpResponse(challenge, status=200)
        else: 
            return HttpResponse('error', status=403)
 
        
    if request.method == "POST":
        data = json.loads(request.body)

        print('11. request',request)
        print('22. data',data)

        if 'object' in data and 'entry' in data:
            print('33. dentro do if')
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
                        print('44. phoneNumber',phoneNumber)
                        print('55. message',message)
                        print('66. sendWhatsAppMessage(phoneNumber, message)',sendWhatsAppMessage(phoneNumber, message))
                except:
                    pass
        print('77. fora de if')
        return HttpResponse('success', status=200)
