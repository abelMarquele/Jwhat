from django.http import HttpResponse
from decouple import config
from django.views.decorators.csrf import csrf_exempt
import requests
import json

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


def send_menu_message(phoneNumber):
    menu_title = "MISAU - Menu de Opções"
    menu_options = [
        "1. Informática",
        "2. Matemática",
        "3. Estatística"
    ]
    menu_message = "{}\n\n{}".format(menu_title, "\n".join(menu_options))

    sendWhatsAppMessage(phoneNumber, menu_message)


def whatsapp_menu_view(request):
    received_message = request.GET.get('message', '')

    options = {
        '1': 'Informática',
        '2': 'Matemática',
        '3': 'Estatística'
    }

    if received_message.lower() == 'menu':
        phoneNumber = "258844680366"  # Substitua pelo número de telefone para o qual deseja enviar o menu
        send_menu_message(phoneNumber)
        response_message = "Um menu de opções foi enviado para você. Por favor, escolha uma opção digitando o número correspondente."
    else:
        response_message = options.get(received_message, 'Opção inválida. Por favor, selecione uma opção válida.')

        if response_message in options.values():
            phoneNumber = "258844680366"  # Substitua pelo número de telefone para o qual deseja enviar a resposta
            sendWhatsAppMessage(phoneNumber, response_message)

    return HttpResponse(response_message)


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
                        if text.lower() == 'menu':
                            send_menu_message(phoneNumber)
                            sendWhatsAppMessage(phoneNumber, "Um menu de opções foi enviado para você. Por favor, escolha uma opção digitando o número correspondente.")
                        else:
                            options = {
                                '1': 'Informática',
                                '2': 'Matemática',
                                '3': 'Estatística'
                            }
                            response_message = options.get(text, 'Opção inválida. Por favor, selecione uma opção válida.')

                            if response_message in options.values():
                                sendWhatsAppMessage(phoneNumber, response_message)
                except:
                    pass

        return HttpResponse('success', status=200)
