import csv

from django.contrib import admin
from django.http import StreamingHttpResponse

from .models import Dictionary


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class DictionaryAdmin(admin.ModelAdmin):
    raw_id_fields = ('room',)
    list_filter = ('room',)

    actions = ['download_csv']

    def download_csv(self, request, queryset):
        queryset = queryset.select_related('room')

        def generator(queryset):
            fields = ('room__name', 'word', 'meaning', 'country')
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            yield 'raum,wort,bedeutung,land\n'
            for row in queryset.values_list(*fields):
                yield writer.writerow(row)

        response = StreamingHttpResponse(
            generator(queryset), content_type='text/csv'
        )
        fn = 'woerterbuch.csv'
        response['Content-Disposition'] = 'attachment; filename="%s"' % fn
        return response
    download_csv.short_description = 'Download CSV'


admin.site.register(Dictionary, DictionaryAdmin)
