import form
from django import forms
from .models import Bug, Project, Profile, BugHistory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'John...',
        }),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        }),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
        }),
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'john@mail.com',
            }),
        }


class ForgotPassword(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email...',
        }),
    )
    class Meta:
        model = Profile
        fields = [
            'email',
        ]


class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter New Password',
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
        }),
    )


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = [
            'title',
            'description',
            'images',
            'assigned_to',
        ]
        exclude = [
            'bug_id',
        ]

    def __init__(self, project, *args, **kwargs):
        # user = kwargs.pop('user')  # Remove the 'user' keyword argument
        super().__init__(*args, **kwargs)
        # self.fields['assigned_to'].queryset = User.objects.exclude(email=user.email)

        creator_user = project.created_user
        associated_user = project.users.all()

        combined_users = associated_user | User.objects.filter(pk=creator_user.pk)

        self.fields['assigned_to'].queryset = combined_users


class ProjectForm(forms.ModelForm):
    users = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
        }),  # Customize the appearance
        help_text="Enter email addresses separated by commas.",
    )
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'users',
        ]


class UpdateBugForm(forms.ModelForm):
    class Meta:
        model = BugHistory
        fields = [
            'comments',
            'images',
            'status',
        ]
