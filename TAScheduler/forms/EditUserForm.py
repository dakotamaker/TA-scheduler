from django import forms
from .EditForm import EditForm

#Edit user information
class EditForm(EditForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    fname = forms.CharField(max_length=50, label='First name',widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    lname = forms.CharField(max_length=50, label='Last name',widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    role_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)


