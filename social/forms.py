#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Dirección de correo electrónico'
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Contraseña (confirmación)',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username','email')    

    def clean_email(self):
        email = self.data.get('email')
        users = User.objects.filter(email=email)
        if email and len(users):
            raise forms.ValidationError('Ya existe un usuario con este email.')
        return email


    def clean_password2(self):        
        password1 = self.data.get('password1')
        password2 = self.data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')            
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)        
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user