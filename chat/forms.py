from django import forms
from django_countries.fields import CountryField

from .models import Room, Presence


class EnterRoomForm(forms.Form):
    room = forms.CharField()
    username = forms.CharField(max_length=255)
    country = CountryField().formfield()

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        room = self.get_room()
        username = self.cleaned_data['username']
        is_present = Presence.objects.is_present(username, room)
        if is_present:
            session = self.session.get(room.room_key, {})
            if session.get('username') != username:
                raise forms.ValidationError('Username schon im Raum')

    def save(self):
        room = self.get_room()
        self.session[room.room_key] = self.get_session_info()
        self.session.modified = True
        return room

    def get_room(self):
        if hasattr(self, '_room'):
            return self._room
        room_name = self.cleaned_data['room']
        self._room, created = Room.objects.get_or_create(
            name__iexact=room_name, defaults={
                'name': room_name
            }
        )
        self.room_created = created
        return self._room

    def get_session_info(self):
        return {
            'username': self.cleaned_data['username'],
            'country': self.cleaned_data['country'],
        }
