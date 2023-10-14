from django.urls import path
from . import views

urlpatterns = [
    path('generate-token/', views.generate_telegram_token, name='generate-telegram-token'),
]
