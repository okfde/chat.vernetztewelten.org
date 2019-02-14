from django.db import models
from django_countries.fields import CountryField

from chat.models import Room


class Dictionary(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    word = models.CharField(max_length=10)
    meaning = models.TextField()
    country = CountryField(blank_label='(wähle dein Land)')

    class Meta:
        verbose_name = 'Wörterbuch-Eintrag'
        verbose_name_plural = 'Wörterbücher-Einträge'

    def __str__(self):
        return '{} in {}'.format(self.word, self.room)
