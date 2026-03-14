from django.urls import path

from .views import TgRegisterAPIView, WebRegisterAPIView

app_name = "auth_user"

urlpatterns = [
    path("tg/register/", TgRegisterAPIView.as_view(), name="tg_register"),
    path("web/register/", WebRegisterAPIView.as_view(), name="web_register"),
]
