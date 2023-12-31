from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django import forms 
from django.forms.widgets import PasswordInput, TextInput

# Registration form
class CreateUserForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ['username','email','password1','password2']
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is used!')
        if len(email) >= 350:
            raise forms.ValidationError('This email is too long!')
        
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class ContactForm(forms.Form):
    subject = forms.CharField(widget=TextInput())
    name = forms.CharField(widget=TextInput())
    email = forms.CharField(widget=TextInput())
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 15}))