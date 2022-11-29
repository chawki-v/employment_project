from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import *
User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ["username","email","password1", "password2"]

class ProfileForm(ModelForm):
    class Meta:
        model = Condidat
        fields = ["age","phone","location", "gender","profession"]



#class RegisterForm(UserCreationForm):
#    age = forms.CharField(max_length=100, help_text='Age ')
#   phone = forms.CharField(max_length=100, help_text='Phone Number ')
#    location = forms.CharField(max_length=100, help_text='Location ')
#    profession = forms.CharField(max_length=100, help_text='Profession ')
#    class Meta:
#        model = User
#        fields = ["first_name","last_name","username", "password1", "password2", "age", "email", "phone", "location","profession",]
