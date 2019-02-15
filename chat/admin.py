from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from .models import Room, Message, delete_old_messages


class RoomAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'


class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('room',)

    def get_urls(self):
        urls = super().get_urls()
        return [
            url(r'^delete-old-messages/$',
                self.admin_site.admin_view(self.delete_old_messages),
                name='chat-message-delete_old'),
        ] + urls

    def delete_old_messages(self, request):
        if not request.method == 'POST':
            raise PermissionDenied
        if not self.has_change_permission(request):
            raise PermissionDenied

        result = delete_old_messages()
        self.message_user(request, 'Alte Nachrichten gelöscht: {}'.format(
            result
        ))
        return redirect('admin:chat_message_changelist')


admin.site.register(Room)
admin.site.register(Message, MessageAdmin)
