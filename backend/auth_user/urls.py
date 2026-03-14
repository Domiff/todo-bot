from django.urls import path

from .views import TgRegisterAPIView

app_name = "auth_user"

urlpatterns = [
    path("tg/register/", TgRegisterAPIView.as_view(), name="register"),
]
