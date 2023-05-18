from django.urls import include, path

from .views import whatsappWebhook, home

urlpatterns = [
    path('', home, name='home'),
    path('whatsapp-webhook/', whatsappWebhook, name='whatsapp_webhook'),
]
