from django import forms

#Edit user information
class EditUserForm(forms.Form):
    for_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    fname = forms.CharField(max_length=50, label='First name',widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    lname = forms.CharField(max_length=50, label='Last name',widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    role_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
    phone = forms.CharField(max_length=50, label='Phone number',widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    office_hours = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    office_location = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)


