# from django.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    last_location = models.PointField(
        verbose_name="last known location",
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    # objects = models.GeoManager()

    def __str__(self):
        return "{}, ({}), last seen at {} ... cr={}, mod={}" \
            .format(self.username, self.get_full_name(), self.last_location, self.created, self.modified)


class FriendGroup(models.Model):
    class Meta:
        verbose_name = "firends list"
        verbose_name_plural = "friends lists"

    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="name"
    )
    owner = models.ForeignKey(
        User,
        related_name="list_owner",
        verbose_name="owner",
        on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        User,
        through='UserFriendGroup'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    # objects = models.Manager()

    def __str__(self):
        return "{} owned by {}".format(self.name, self.owner)


class UserFriendGroup(models.Model):
    class Meta:
        unique_together = ['member', 'friend_group']
        verbose_name = "friend group members"
        verbose_name_plural = "friend group members"

    member = models.ForeignKey(
        User,
        verbose_name="member",
        on_delete=models.CASCADE
    )
    friend_group = models.ForeignKey(
        FriendGroup,
        verbose_name="friend group",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    # objects = models.Manager()

    def __str__(self):
        return "{} is a member of {}".format(self.member, self.friend_group)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
