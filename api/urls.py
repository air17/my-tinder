from django.urls import path
from accounts.views import UserCreate
from api.views import match, UserList, UserLocationUpdate, UserRetrieve

urlpatterns = [
    path('clients/create/', UserCreate.as_view()),
    path('clients/<uuid:pk>/match/', match),
    path('list/', UserList.as_view()),
    path('clients/<uuid:pk>/location/', UserLocationUpdate.as_view()),
    path('clients/<uuid:pk>/', UserRetrieve.as_view()),
]
