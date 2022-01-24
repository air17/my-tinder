from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "first_name", "last_name", "sex", "picture")
