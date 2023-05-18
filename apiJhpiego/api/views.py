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


def handle_menu_choice(phoneNumber, choice):
    response_message = ""

    if choice == '1':
        response_message = "Informática"
    elif choice == '2':
        response_message = "Matemática"
    elif choice == '3':
        response_message = "Estatística"
    else:
        response_message = "Opção inválida. Por favor, escolha uma opção válida."

    sendWhatsAppMessage(phoneNumber, response_message)

    secondary_menu_options = [
        "1. Voltar ao Menu Anterior",
        "0. Terminar Conversa"
    ]
    send_menu_message(phoneNumber, secondary_menu_options)


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
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        if text == '0':
                            sendWhatsAppMessage(phoneNumber, "Conversa encerrada. Obrigado!")
                            return HttpResponse('success', status=200)
                        elif text in ['1', '2', '3']:
                            handle_menu_choice(phoneNumber, text)
                        elif text == '1. Voltar ao Menu Anterior':
                            main_menu_options = [
                                "1. Abel",
                                "2. Belito",
                                "3. Marquele",
                                "0. Terminar Conversa"
                            ]
                            send_menu_message(phoneNumber, main_menu_options)
                        else:
                            sendWhatsAppMessage(phoneNumber, "Opção inválida. Por favor, escolha uma opção válida.")

                except:
                    pass

        return HttpResponse('success', status=200)


def atendimento_cliente_view(request):
    phoneNumber = "258844680366"  # Substitua pelo número de telefone de atendimento

    main_menu_options = [
        "1. Abel",
        "2. Belito",
        "3. Marquele",
        "0. Terminar Conversa"
    ]
    send_menu_message(phoneNumber, main_menu_options)

    return HttpResponse("Bem-vindo ao atendimento ao cliente. Um menu de opções foi enviado para você. Por favor, escolha uma opção digitando o número correspondente.")


