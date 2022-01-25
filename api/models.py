from django.contrib.auth import get_user_model
from django.db import models


class Match(models.Model):
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_from")
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_to")
    created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user1', 'user2',)

    def __str__(self):
        return self.user1.__str__() + " likes " + self.user2.__str__()
