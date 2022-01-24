from django.urls import path
from accounts.views import UserCreate

urlpatterns = [
    path('clients/create/', UserCreate.as_view(), name='user-create'),
]
