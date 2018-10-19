from django import forms


class UploadFileForm(forms.Form):
    image_file = forms.FileField()
