from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class UserProfileForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'name@gmail.com'}),required=True,label='Email')
    
    class Meta:
        model = UserProfile
        fields = ('email','password1','password2')
        