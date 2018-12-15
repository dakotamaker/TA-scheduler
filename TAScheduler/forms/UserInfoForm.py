from django import forms


class UserInfoForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    fname = forms.CharField(max_length=50, label='First name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    lname = forms.CharField(max_length=50, label='Last name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    role_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=50, label='Phone number',widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_hours = forms.CharField(max_length=50, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_location = forms.CharField(max_length=50, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))