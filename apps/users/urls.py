from django.urls import path
from .views import UserListCreateView, GetUserToken, UserRegistrationView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('get-telegram-token/', GetUserToken.as_view(), name='get-telegram-token'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]