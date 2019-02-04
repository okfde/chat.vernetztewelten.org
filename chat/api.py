from channels.db import database_sync_to_async

from .models import Room, Message, Presence
from .serializers import RoomSerializer, MessageSerializer


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
    messages = Message.objects.filter(room=room)[:50]
    userlist = _get_userlist(room)
    return RoomSerializer({
        'name': room.name,
        'messages': messages,
        'userlist': userlist
    }).data


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
