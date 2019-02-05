from django.contrib import admin

from .models import Dictionary


class DictionaryAdmin(admin.ModelAdmin):
    raw_id_fields = ('room',)


admin.register(Dictionary, DictionaryAdmin)
