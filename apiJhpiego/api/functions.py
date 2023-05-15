# from django.conf import settings
# import requests


# def sendWhatsAppMessage(phoneNumber, messege):
#     headers = {"Authorization": settings.WHATSAPP_TOKEN}
#     payload = {
#                 "messaging_product": "whatsapp",
#                 "recipient_type": "individual",
#                 "to": phoneNumber, 
#                 "type": "text", 
#                 "text": { "body":messege} 

#                }
#     response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
#     ans = response.json()
#     print('111. headers',headers)
#     print('222. payload',payload)
#     print('333. response',response)
#     print('444. ans',ans)
#     return ans

import requests

WHATSAPP_URL = 'https://graph.facebook.com/v16.0/103297242770340/messages'
WHATSAPP_TOKEN = 'Bearer EAACwv64kYI4BANuE0cOJyuBvCuGywNtGg39zO54bRVSuBWQLzZBNd0IhpPvPR1U9qNbPOxiiaUddQPANY0ZCrQn88NlEALzLtDsDr366UMwFdjRIjuVf9IWpui3GUncLGWdn4I8Lpc8tVGdBZC7GxcV9HIZBradKfG23u4gCakR0YOpC9ZB8uc2EQ6ciSsJoLc3CIXS3QZAzI9brQDEAv9'

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


