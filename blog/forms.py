from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, Textarea, EmailInput, PasswordInput

from blog.models import Comment


User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Username',
                                         'style': 'width: 300px;',
                                         'class': 'form-control'
                                         }),
                    }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'text']
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Username',
                                         'style': 'width: 300px;',
                                         'class': 'form-control'
                                         }),
            'text': Textarea(attrs={'class': 'form-control',
                                    'label': 'Text'})
        }


class ContactUsForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Message', required=True)
