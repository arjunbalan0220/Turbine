# accounts/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import RegistrationForm

class Registration(forms.ModelForm):
    fname = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    mname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}),required=False)
    lname = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone'}),min_length=10,max_length=11)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), min_length=8)
    

    class Meta:
        model = RegistrationForm
        fields = ['fname', 'mname', 'lname', 'email', 'phone', 'password']  # Include specific fields
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RegistrationForm.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address is already registered.")
        if "@" not in email:
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        self.validate_password_strength(password)
        return password

    def validate_password_strength(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
