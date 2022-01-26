from django.contrib.auth import get_user_model
from rest_framework.fields import FloatField
from rest_framework.serializers import ModelSerializer


class ThinUserSerializer(ModelSerializer):
    distance = FloatField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "sex", "picture",
                  "latitude", "longitude", "distance")


class UpdateUserLocationSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("latitude", "longitude")
