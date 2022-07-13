from logging import PlaceHolder
from django import forms
import re
from django.core.exceptions import ValidationError


class UrlForm(forms.Form):

    url = forms.CharField(label='Enter URL :', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search ..'}))

    def clean_url(self):
        data = self.cleaned_data['url']
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        if not re.match(regex,data):
            raise ValidationError("Enter correct url.")
        return data