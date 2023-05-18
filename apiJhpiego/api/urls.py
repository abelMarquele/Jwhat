from django.urls import include, path
from rest_framework import routers

from .views import whatsappWebhook

from apiJhpiego.views import UserViewSet, GroupViewSet, home

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
# router.register(r'home', views.HomeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', home, name='home'),
    path('whatsapp-webhook/', whatsappWebhook, name='whatsapp_webhook'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#Callback URL
# https://jwhat.herokuapp.com/whatsapp-webhook

#Verify token
# whatsapp-webhook