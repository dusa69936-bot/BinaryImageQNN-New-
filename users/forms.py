from django import forms
from .models import UserRegistrationModel


class UserRegistrationForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={'pattern': '[A-Za-z ]+'}),
        required=True,
        max_length=100
    )

    loginid = forms.CharField(
        widget=forms.TextInput(attrs={'pattern': '[A-Za-z0-9]+'}),
        required=True,
        max_length=100
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
            'title': 'Must contain one number, one uppercase, one lowercase and 8 characters'
        }),
        required=True,
        max_length=100
    )

    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'pattern': '[6-9][0-9]{9}'}),
        required=True,
        max_length=100
    )

    email = forms.CharField(
        widget=forms.EmailInput(),
        required=True,
        max_length=100
    )

    locality = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        max_length=100
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows':4}),
        required=True,
        max_length=250
    )

    city = forms.CharField(
        widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+'}),
        required=True,
        max_length=100
    )

    state = forms.CharField(
        widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+'}),
        required=True,
        max_length=100
    )

    status = forms.CharField(
        widget=forms.HiddenInput(),
        initial="activated"
    )


    class Meta:

        model = UserRegistrationModel

        fields = "__all__"