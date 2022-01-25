from django.core.mail import send_mail, EmailMessage
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
from api.models import Match


def send_match_email(user1, user2):
    email1 = EmailMessage(subject='You\'ve got a new match!')
    email1.body = f'{user1.get_full_name()} likes you! Their email: {user1.email}'
    email1.to = [user2.email]
    email1.send(fail_silently=True)

    email2 = EmailMessage(subject='You\'ve got a new match!')
    email2.body = f'{user2.get_full_name()} likes you! Their email: {user2.email}'
    email2.to = [user1.email]
    email2.send(fail_silently=True)


@api_view(['POST'])
def match(request, pk, **kwargs):
    if request.user.is_anonymous:
        return Response({"text": "Log in, please!"}, status=status.HTTP_403_FORBIDDEN)
    user_from = User.objects.get(pk=request.user.id)
    user_to = User.objects.get(pk=pk)
    if user_from == user_to:
        return Response({"text": "You can't like yourself"}, status=status.HTTP_409_CONFLICT)
    try:
        Match.objects.create(user1=user_from, user2=user_to)
    except IntegrityError:
        return Response({"text": "You already liked this user"}, status=status.HTTP_409_CONFLICT)
    else:
        is_match = Match.objects.filter(user1=user_to, user2=user_from)
        if is_match:
            send_match_email(user_from, user_to)
            return Response({"match": True,
                             "text": f"It's a match! Their email: {user_to.email}"})
        else:
            return Response({"match": False,
                             "text": ""})
