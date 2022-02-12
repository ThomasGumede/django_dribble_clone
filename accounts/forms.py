from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)

User = get_user_model()

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(error_messages={'required': 'Sorry, please enter your username'}, widget=forms.TextInput(
        attrs={'id': 'login__username',
        'placeholder': 'Username'}))
    password = forms.CharField(error_messages={'required': 'Sorry, please enter your password'}, widget=forms.PasswordInput(
        attrs={
            
            'id': 'login__password',
            'placeholder': 'Password'
        }
    ))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        
        if not user.exists():
            raise forms.ValidationError('This username doesn\'t exist, please provide a valid username')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        user = User.objects.get(username=username)
        if user.check_password(password):
            return password

        raise forms.ValidationError('Your password is incorrect')

class RegistrationForm(UserCreationForm):
    """
    Registration Form - create new user using username, email and password
    """

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("This email already exists")
        return email

class PwdResetForm(PasswordResetForm):
    """
    Custom password reset form
    """

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'id': 'reset_form_email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Unfortunatley we can not find this email address')
        if not User.objects.get(email=email).is_active:
            raise forms.ValidationError('Unfortunatley, your email address is not verified')

        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'New password', 'id': 'reset_form_newpassword'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Retype-New password', 'id': 'reset_form_newpassword2'}))

class AccountUpdateForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'photo', 'biography', 'website', 'location']

class GeneralEditForm(forms.ModelForm):
    """
        Form to edit only username and email
    """
    class Meta:
        model = User
        fields = ["username", "email"]