from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from accounts.serializers import UserSerializer


class UserCreate(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
