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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_charter(self):        
        import math

        charter = self.data.get('charter')

        if not charter:
            return charter

        if not charter.isnumeric:
            raise forms.ValidationError('Ingrese una cédula válida.')

        if len(charter) != 10:
            raise forms.ValidationError('Ingrese una cédula válida.')

        total = 0
        digit = (int(charter[9])*1)

        for i in range(len(charter) - 2):
            mult = 0;
            if ( i%2 ) != 0:
                total = total + ( int(charter[i]) * 1 )
            else:
                mult = int(charter[i]) * 2
                if mult > 9:
                    total = total + ( mult - 9 )
                else: 
                    total = total + mult;

        decena = total / 10
        decena = math.floor( decena )
        decena = ( decena + 1 ) * 10
        final = decena - total

        if ( final == 10 and digit == 0 ) or ( final or digit ):
            return charter
        
        raise forms.ValidationError('Ingrese una cédula válida.')
