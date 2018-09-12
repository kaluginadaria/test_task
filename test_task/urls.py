from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from habr.views import jwt_response_payload_handler

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('habr.api.urls')),
]
