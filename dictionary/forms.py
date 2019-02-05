from django import forms
from django_countries.fields import CountryField

from .models import Dictionary
from .utils import get_first_emoji


class DictionaryForm(forms.Form):
    word = forms.CharField(max_length=25)
    meaning = forms.CharField(max_length=1024)
    country = CountryField().formfield()

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)

    def clean_word(self):
        word = self.cleaned_data['word']
        em = get_first_emoji(word)
        if em is None:
            raise forms.ValidationError('Kein Emoji!')
        return em

    def save(self, room):
        return Dictionary.objects.create(
            room=room,
            word=self.cleaned_data['word'],
            meaning=self.cleaned_data['meaning'],
            country=self.cleaned_data['country'],
        )