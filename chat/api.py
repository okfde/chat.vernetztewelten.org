from channels.db import database_sync_to_async

from dictionary.models import Dictionary
from dictionary.forms import DictionaryForm
from dictionary.serializers import DictionarySerializer

from .models import Room, Message, Presence
from .serializers import RoomSerializer, MessageSerializer

# Synchronize with Room.vue
MESSAGE_COUNT = 50


@database_sync_to_async
def get_room(room_uid):
    try:
        return Room.objects.get(uuid=room_uid)
    except Room.DoesNotExist:
        return None


@database_sync_to_async
def get_room_info(room_uid=None, room=None):
    if room is None:
        room = Room.objects.get(uuid=room_uid)
    messages = Message.objects.filter(room=room)[:MESSAGE_COUNT]
    userlist = _get_userlist(room)
    return RoomSerializer({
        'name': room.name,
        'messages': messages,
        'userlist': userlist,
        'dictionary': _get_dictionary(room)
    }).data


@database_sync_to_async
def get_message_list(room, before_date):
    messages = Message.objects.filter(
        room=room,
        timestamp__lt=before_date
    )[:MESSAGE_COUNT]
    return MessageSerializer(messages, many=True).data


@database_sync_to_async
def get_userlist(room):
    return _get_userlist(room)


def _get_userlist(room):
    return list(Presence.objects.list_users(room))


@database_sync_to_async
def update_presence(username, room, **kwargs):
    Presence.objects.touch(
        username, room, **kwargs
    )


@database_sync_to_async
def remove_presence(username, room):
    Presence.objects.remove(
        username, room
    )
    return _get_userlist(room)


@database_sync_to_async
def add_message(username, room, message):
    message = Message.objects.create(
        username=username,
        room=room,
        message=message
    )
    return MessageSerializer(message).data


@database_sync_to_async
def add_dictionary_entry(room, country, word, meaning):
    form = DictionaryForm(data={
        'word': word,
        'meaning': meaning,
        'country': country
    })
    if form.is_valid():
        form.save(room)
    return DictionarySerializer(
        _get_dictionary(room),
        many=True
    ).data


def _get_dictionary(room):
    return Dictionary.objects.filter(room=room).values(
        'id', 'word', 'meaning', 'country'
    )
