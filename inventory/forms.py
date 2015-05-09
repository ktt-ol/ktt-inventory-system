from django import forms


class UploadFileForm(forms.Form):

    types = (('1', 'Parent Tree'), ('2', 'Regal'))

    file = forms.FileField()
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=types)