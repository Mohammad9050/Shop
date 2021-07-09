from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from Accounts.models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Re-enter password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ChangeForm(UserChangeForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'pay-style'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'pay-style'}))
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name']

    password = None
