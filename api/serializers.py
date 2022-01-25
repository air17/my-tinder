from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class ThinUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "sex", "picture")
