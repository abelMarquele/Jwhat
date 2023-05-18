from django.http import HttpResponse
from decouple import config
from django.views.decorators.csrf import csrf_exempt
import requests
import json

WHATSAPP_URL = 'https://graph.facebook.com/v16.0/103297242770340/messages/'

def send_message(phone_number, message):
    # token = 'SEU_TOKEN_AQUI'  # Substitua pelo seu token de acesso do WhatsApp
    token = config('WHATSAPP_TOKEN', default='')
    headers = {"Authorization": token}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        ans = response.json()
        return ans
    else:
        return "Erro ao enviar mensagem: " + response.text


def send_menu_message(phone_number, menu_options):
    menu_title = "MISAU - Menu de Opções"
    menu_message = "{}\n\n{}".format(menu_title, "\n".join(menu_options))

    send_message(phone_number, menu_message)


def handle_menu_choice(phone_number, choice):
    response_message = ""

    if choice == '1':
        response_message = "Informática"
    elif choice == '2':
        response_message = "Matemática"
    elif choice == '3':
        response_message = "Estatística"
    else:
        response_message = "Opção inválida. Por favor, escolha uma opção válida."

    send_message(phone_number, response_message)

    secondary_menu_options = [
        "1. Voltar ao Menu Anterior",
        "0. Terminar Conversa"
    ]
    send_menu_message(phone_number, secondary_menu_options)


@csrf_exempt
def whatsappWebhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                for entry in data['entry']:
                    try:
                        phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        if text == '0':
                            send_message(phoneNumber, "Conversa encerrada. Obrigado!")
                        elif text == '1' or text == '2' or text == '3':
                            handle_menu_choice(phoneNumber, text)
                        elif text == '9':
                            main_menu_options = [
                                "1. Abel",
                                "2. Belito",
                                "3. Marquele",
                                "0. Terminar Conversa"
                            ]
                            send_menu_message(phoneNumber, main_menu_options)
                        else:
                            send_message(phoneNumber, "Opção inválida. Por favor, escolha uma opção válida.")

                    except Exception as e:
                        print(f"Erro ao processar mensagem: {e}")
        
        return HttpResponse('success', status=200)

    elif request.method == 'GET':
        return HttpResponse("Webhook configurado com sucesso!")
