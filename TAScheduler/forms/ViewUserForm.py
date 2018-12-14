from django import forms

#Edit user information
class ViewUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))



