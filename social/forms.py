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
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['is_commercial', 'is_complete']

    first_name = forms.CharField(max_length=30, label='Nombres') 
    last_name = forms.CharField(max_length=30, label='Apellidos')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        self.fields['charter'].required = True
        self.fields['cellphone'].required = True

    def clean_charter(self):        
        import math

        charter = self.data.get('charter')

        valid, message = validate_charter(charter)

        if not valid:
            raise forms.ValidationError(message)

        return charter

    def save(self, username=None, email=None, commit=True):
        obj = super(ProfileForm, self).save(commit=False)
        obj.is_complete = True

        obj.user.first_name = self.cleaned_data['first_name']
        obj.user.last_name = self.cleaned_data['last_name']
        if username is not None: obj.user.username = username
        if email is not None: obj.user.email = email

        obj.user.save()
        
        if commit:
            obj.save()
        return obj


def validate_charter(charter):
    if charter is None:
        return (False, 'Este campo es requerido.')        
    if not charter.isdigit:
        return (False, 'Ingrese una cédula válida.')        
    if len(charter) != 10:
        return (False, 'La cédula debe contener 10 dígitos numéricos.')        

    total = 0
    coeficientes = (2,1,2,1,2,1,2,1,2,)
    
    verificador_recibido = int(charter[9])
    for i, cf in enumerate(coeficientes):        
        mult = int(charter[i]) * cf
        total = total + mult if mult <= 9 else total + ( mult - 9 )

    band = total%10    
    verificador_obtenido = total if total < 10 else 10 - band if band != 0  else band

    if verificador_recibido == verificador_obtenido:
        return (True, None)
    
    return (False, 'Ingrese una cédula válida.')
