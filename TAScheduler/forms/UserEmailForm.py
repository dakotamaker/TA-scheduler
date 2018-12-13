from django import forms

class UserEmailForm(forms.Form):
    email = forms.EmailField()