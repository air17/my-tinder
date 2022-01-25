from django.urls import path
from accounts.views import UserCreate
from api.views import match, UserList

urlpatterns = [
    path('clients/create/', UserCreate.as_view(), name='user-create'),
    path('clients/<uuid:pk>/match/', match),
    path('list/', UserList.as_view())
]
