import form
from django import forms
from .models import Bug, Project, Profile
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class ForgotPassword(PasswordResetForm):
    class Meta:
        model = Profile
        fields = ['email']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }

class PasswordResetForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description', 'images', 'assigned_to']
        exclude = ['bug_id']

    def __init__(self, project, *args, **kwargs):
        # user = kwargs.pop('user')  # Remove the 'user' keyword argument
        super().__init__(*args, **kwargs)
        # self.fields['assigned_to'].queryset = User.objects.exclude(email=user.email)
        self.fields['assigned_to'].queryset = project.users.all()

class ProjectForm(forms.ModelForm):
    users = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),  # Customize the appearance
        help_text="Enter email addresses separated by commas."
    )
    class Meta:
        model = Project
        fields = ['name', 'description', 'users']

