from django import forms

class ImageForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    image = forms.ImageField()
    encrypt = forms.BooleanField(required=False)
