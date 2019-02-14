from datetime import timedelta
import json
import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone

from django_countries.fields import CountryField

MAX_AGE = timedelta(seconds=60)


class Room(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Raum'
        verbose_name_plural = 'Räume'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_uuid': str(self.uuid)})

    @property
    def room_key(self):
        return 'room_%s' % self.uuid


class PresenceManager(models.Manager):
    def touch(self, username, room, **kwargs):
        kwargs['last_seen'] = timezone.now()
        Presence.objects.update_or_create(
            username=username,
            room=room,
            defaults=kwargs
        )

    def get_present(self, room):
        return Presence.objects.filter(
            room=room,
            last_seen__gte=timezone.now() - MAX_AGE
        )

    def is_present(self, username, room):
        return self.get_present(room).filter(username=username).exists()

    def list_users(self, room):
        return self.get_present(room).values('username', 'country')

    def remove(self, username, room):
        Presence.objects.filter(
            username=username,
            room=room
        ).delete()

    def expire(self):
        Presence.objects.filter(
            last_seen__lt=timezone.now() - MAX_AGE
        ).delete()


class Presence(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    last_seen = models.DateTimeField(default=timezone.now)
    country = CountryField()

    objects = PresenceManager()

    def __str__(self):
        return '{} in {} at {}'.format(
            self.username, self.room, self.last_seen
        )

    def get_context(self):
        if not self.context:
            return {}
        return json.loads(self.context)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return '{} in {} um {}'.format(
            self.username, self.room, self.timestamp
        )
