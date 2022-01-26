from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models.expressions import RawSQL
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Match
from api.serializers import ThinUserSerializer, UpdateUserLocationSerializer

User = get_user_model()


def _send_match_email(user1, user2):
    email1 = EmailMessage(subject='You\'ve got a new match!')
    email1.body = f'{user1.get_full_name()} likes you! Their email: {user1.email}'
    email1.to = [user2.email]
    email1.send(fail_silently=True)

    email2 = EmailMessage(subject='You\'ve got a new match!')
    email2.body = f'{user2.get_full_name()} likes you! Their email: {user2.email}'
    email2.to = [user1.email]
    email2.send(fail_silently=True)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def match(request, pk, **kwargs):
    user_from = User.objects.get(pk=request.user.id)
    user_to = User.objects.get(pk=pk)

    if user_from == user_to:
        return Response({"text": "You can't like yourself"}, status=status.HTTP_409_CONFLICT)

    try:
        Match.objects.create(user1=user_from, user2=user_to)
    except IntegrityError:
        return Response({"text": "You already liked this user"}, status=status.HTTP_409_CONFLICT)
    else:
        matches = Match.objects.filter(user1=user_to, user2=user_from)
        if matches:
            _send_match_email(user_from, user_to)
            return Response({"match": True,
                             "text": f"It's a match! Their email: {user_to.email}"})
        else:
            return Response({"match": False,
                             "text": ""})


class UserFilter(filters.FilterSet):
    distance = filters.NumberFilter(label="Distance", lookup_expr="lt")
    first_name = filters.CharFilter(lookup_expr="contains")
    last_name = filters.CharFilter(lookup_expr="contains")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'sex', 'distance']


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ThinUserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        longitude = request.user.longitude
        latitude = request.user.latitude
        if longitude and latitude:
            self.queryset = _annotate_distance(self.queryset, latitude, longitude)
        elif request.query_params.get("distance"):
            return Response({"text": "You should specify your location to filter by distance"},
                            status=status.HTTP_400_BAD_REQUEST)
        return self.list(request, *args, **kwargs)


def _annotate_distance(queryset, latitude, longitude):
    # Great circle distance formula
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"

    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    return queryset.annotate(distance=distance_raw_sql)


class UserLocationUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserLocationSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieve(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ThinUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        longitude = request.user.longitude
        latitude = request.user.latitude
        if longitude and latitude:
            self.queryset = _annotate_distance(self.queryset, latitude, longitude)
        return self.retrieve(request, *args, **kwargs)
