from django.urls import include, path
from rest_framework import routers
from apiJhpiego.api import views
from apiJhpiego.views import UserViewSet, GroupViewSet, home

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
# router.register(r'home', views.HomeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('', home, name='home'),
    path('whatsapp-webhook', views.whatsappWebhook, name= 'whatsapp-webhook'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#Callback URL
# https://jwhat.herokuapp.com/whatsapp-webhook

#Verify token
# whatsapp-webhook