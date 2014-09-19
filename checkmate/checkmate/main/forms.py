from django import forms
from checkmate.main.models import *

# Create your tests here.

class AnswerForm(forms.Form):
	answer=forms.CharField()
	dd=forms.BooleanField(required=False)

class MarketForm(forms.Form):
	flip=forms.IntegerField(initial=0,min_value=0)
	dd=forms.IntegerField(initial=0,min_value=0)

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 50)
	password=forms.CharField(widget=forms.PasswordInput())

class RegistrationForm(forms.Form):
	username=forms.CharField(max_length=50,label='Team Name (Username):')
	password=forms.CharField(widget=forms.PasswordInput(),max_length=50)
	name1=forms.CharField(max_length=50,label='Name of 1st Participant :')
	name2=forms.CharField(max_length=50,required=False,label='Name of 2nd Participant :')
	phone1=forms.IntegerField(widget=forms.TextInput(),min_value=6000000000,label='Phone of 1st Participant :')
	phone2=forms.IntegerField(widget=forms.TextInput(),required=False,min_value=6000000000,label='Phone of 2nd Participant :')
	email1=forms.EmailField(label='Email of 1st Participant :')
	email2=forms.EmailField(required=False,label='Email of 2nd Participant :')