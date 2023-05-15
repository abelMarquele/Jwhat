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

# import requests

# WHATSAPP_URL = 'https://graph.facebook.com/v16.0/103297242770340/messages'
# WHATSAPP_TOKEN = 'Bearer EAACwv64kYI4BAHaWJwUUzZBMA93EAKO4ygH0N6w2FikZBhRfQcpRG10o6ZBBkUGrj6tzInl1Smtfni8XJSvkjaJ8NzDoKZBYaiCAaoZAlPhtslIKfbedwS2SxdumOIi8HxjSkZC5jCwoIosqhsQLp3tLBtvWfGBgr7VfGcoUrc0BRv1flSdTf2RPgbhk7QgtqbipzyECpOZB30oo653VJNP'

# def sendWhatsAppMessage(phoneNumber, message):
#     headers = {"Authorization": WHATSAPP_TOKEN}
#     payload = {
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": phoneNumber,
#         "type": "text",
#         "text": {"body": message}
#     }
#     response = requests.post(WHATSAPP_URL, headers=headers, json=payload)
#     if response.status_code == 200:
#         return "Mensagem enviada com sucesso!"
#     else:
#         return "Erro ao enviar mensagem: " + response.text


# # Exemplo de uso:
# phoneNumber = "258844680366"
# message = "Olá! Esta é uma mensagem de teste."
# result = sendWhatsAppMessage(phoneNumber, message)
# print(result)


