import dateutil.parser

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .api import (
    get_room, get_room_info, update_presence, remove_presence,
    add_message, get_userlist, add_dictionary_entry,
    get_message_list
)


class ChatConsumer(AsyncJsonWebsocketConsumer):

    @property
    def user(self):
        if not self.room:
            return
        session = self.scope["session"]
        return session.get(self.room.room_key)

    async def connect(self):
        self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
        self.room = await get_room(self.room_uuid)
        if self.room is None:
            await self.close()
            return

        if self.user is None:
            await self.close()
            return

        self.room_group_name = self.room.room_key

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await update_presence(
            self.user['username'], self.room,
            country=self.user['country']
        )

        userlist = await get_userlist(self.room)
        await self.send_userlist(userlist)

        room_info = await get_room_info(room=self.room)
        room_info['session'] = self.user
        await self.send_json(room_info)

    async def send_userlist(self, userlist, action='joined'):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'userlist',
                'userlist': userlist,
                'user': {
                    'action': action,
                    'username': self.user['username'],
                    'country': self.user['country']
                }
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        if self.user:
            userlist = await remove_presence(self.user['username'], self.room)
            await self.send_userlist(userlist, action='left')

    # Receive message from WebSocket
    async def receive_json(self, content):
        if not self.user:
            return

        if content['type'] == 'hearbeat':
            await update_presence(
                self.user['username'], self.room,
                country=self.user['country']
            )
            return

        if content['type'] == 'list_messages':
            await self.list_messages(content)
            return

        if content['type'] == 'message':
            await self.add_message(content)

        if content['type'] == 'dictionary_entry':
            await self.add_dictionary_entry(content)
            return

    async def list_messages(self, content):
        try:
            before_date = dateutil.parser.parse(content['before'])
        except ValueError:
            return

        messages = await get_message_list(self.room, before_date)
        await self.send_json({
            'moremessages': messages
        })

    async def add_message(self, content):
        message = await add_message(
            self.user['username'],
            self.room,
            content['message']
        )
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def add_dictionary_entry(self, content):
        dictionary = await add_dictionary_entry(
            self.room,
            self.user['country'],
            content['entry'].get('word', ''),
            content['entry'].get('meaning', ''),
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'dictionary_entry',
                'dictionary': dictionary,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send_json({
            'messages': [message]
        })

    async def userlist(self, event):
        await self.send_json({
            'userlist': event['userlist'],
            'user': event['user']
        })

    async def dictionary_entry(self, event):
        await self.send_json({
            'dictionary': event['dictionary']
        })
