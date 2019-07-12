from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import validate_email

from .models import Anuncio
#from .models import Usuario

#Classe que ira gerar o form do Cadastro do CRUD
class AnuncioForm(ModelForm):
    class Meta:
        model = Anuncio #Instancia um objeto do tipo anuncio
        fields = [
            'titulo',
            'descricao',
            'preco',
            'categoria',
            'imgPath',
            'usuario'
        ]

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        #cria uma instancia do model de usuarios do Django admin
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    
    #Salva os dados no formulario
    def save(self, commit=True):

        usuario = super(RegistrationForm, self).save(commit=False)
        
        #self.cleaned_data garante que ninguem injete sql no seu model
        usuario.first_name = self.cleaned_data['first_name']
        usuario.last_name = self.cleaned_data['last_name']
        usuario.email = self.cleaned_data['email']

        if commit:
            usuario.save()

        return usuario

