"""whatsapp_api URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/3.2/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from wabot.views import (
    SendMessageAPIView,
)


router = routers.SimpleRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="WhatsApp API",
        default_version='v1',
        description="WhatsApp API to send whatsapp messages.",
        terms_of_service="https://www.app.intexfy.com/policies/terms/",
        contact=openapi.Contact(email="alves.engleandro@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# [STANDARD-DJANGO]
urlpatterns = [
    path('admin/', admin.site.urls),
]

# [SWAGGER-DOCUMENTATION]
urlpatterns += [
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# [WHATSAPP-ENDPOINTS]
urlpatterns += [
    path('wabot/send-message', SendMessageAPIView.as_view(), name="wabot-send-message"),
]

urlpatterns += router.urls

