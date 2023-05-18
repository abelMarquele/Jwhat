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


def send_menu_message(phoneNumber, menu_options):
    menu_title = "MISAU - Menu de Opções"
    menu_message = "{}\n\n{}".format(menu_title, "\n".join(menu_options))

    sendWhatsAppMessage(phoneNumber, menu_message)


def whatsapp_menu_view(request):
    phoneNumber = "258844680366"  # Substitua pelo número de telefone para o qual deseja enviar o menu

    main_menu_options = [
        "1. Abel",
        "2. Belito",
        "3. Marquele",
        "0. Terminar Conversa"
    ]
    send_menu_message(phoneNumber, main_menu_options)

    return HttpResponse("Um menu de opções foi enviado para você. Por favor, escolha uma opção digitando o número correspondente.")


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
                        response_message = ""

                        if text == '1':
                            response_message = "Informática"
                        elif text == '2':
                            response_message = "Matemática"
                        elif text == '3':
                            response_message = "Estatística"
                        elif text == '0':
                            sendWhatsAppMessage(phoneNumber, "Você terminou a conversa. Obrigado!")
                            return HttpResponse('success', status=200)
                        else:
                            response_message = "Opção inválida. Por favor, escolha uma opção válida."

                        sendWhatsAppMessage(phoneNumber, response_message)

                        secondary_menu_options = [
                            "1. Voltar ao Menu Anterior",
                            "0. Terminar Conversa"
                        ]
                        send_menu_message(phoneNumber, secondary_menu_options)
                except:
                    pass

        return HttpResponse('success', status=200)
