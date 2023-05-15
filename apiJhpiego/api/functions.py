from django.conf import settings
import requests



def sendWhatsAppMessage(phoneNumber, messege):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phoneNumber, 
                "type": "text", 
                "text": { "body":messege} 

               }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json()
    return ans


    # phoneNumber = "258844680366"

    # messege = "Ola Abel, n\ Essa mensagem é de teste"

    # sendWhatsAppMessage(phoneNumber, messege)


