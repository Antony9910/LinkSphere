from django.contrib.auth.models import User #import user models
from django.contrib.auth.forms import UserCreationForm #import usercreationForm for registation
from django import forms
from SocialApp.models import UserProfile

class RegistrationForm(UserCreationForm):
    
    class Meta:
        
        model=User
        fields=["username","email","password1","password2"]
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user','following','block')
        widgets={"dob":forms.DateInput(attrs={"class":"form-control","type":"dat"})}
