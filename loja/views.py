import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User #Importa o model de usuarios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User #Importa o model de usuarios
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


#importa os metodos de acesso ao banco de dados
from .models import Anuncio, Compra, Categoria
from .form import AnuncioForm, RegistrationForm

#Sintaxe do print
#print(request.user.email)

#-----------------------------------------------------------------------------------------
def index(request):
    return render(request, 'loja/login.html')

#-----------------------------------------------------------------------------------------
#So aceita tentativas de login via POST
@csrf_protect
#@login_required(login_url='url_index')
def login_user(request):    
    if request.POST:
        usuario = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(username=usuario, password = senha)

        if user is not None:
            login(request, user)
            return redirect('url_home')
        else:
            #Ver como usar essa mensagem na aula 2 do curso de Django de 37minutos, salvei nos favoritos
            messages.error(request, 'Usuário ou senha incoretos')
        
    return redirect('url_index')

#-----------------------------------------------------------------------------------------
def logout_user(request):
    print(request.user.email)
    logout(request)
    return redirect('url_index')

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def home(request):
    dados = {}
    dados['anuncios'] = Anuncio.objects.all()
    dados['categorias'] = Categoria.objects.all()
    dados['usuario'] = request.user
    #print(dados['anuncios'].query) #Exibe no terminal
    return render(request, 'loja/home.html', dados)

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def minha_conta(request):
    #select * from Anuncio
    dados = {}
    # dados['anuncios'] = Anuncio.objects.all()
    dados['anuncios'] = Anuncio.objects.filter(usuario = request.user)
    dados['usuario'] = request.user
    return render(request, 'loja/minha_conta.html', dados)

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def cadastrar_anuncio(request):
    dados = {}
    if request.method == 'POST':
        #Verifica se ja tem algo no form, se tiver o form já avi p a view com as informações existentes (como um fieldset)
        form = AnuncioForm(request.POST or None, request.FILES)
        form.fields['usuario'].initial = request.user
        #valida o form
        if form.is_valid():
            form.save()
            #Redirect para o metodo minha_conta sem duplicar dados de cadastro e na url certa
            return redirect('url_minha_conta')

    dados['form'] = AnuncioForm()
    dados['usuario'] = request.user
    dados['titulo'] = "Cadastrar Anúncio"
    return render(request, 'loja/form.html', dados)

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def atualizar_anuncio(request, pk):
    dados = {}
    anuncio = Anuncio.objects.get(pk=pk)
    oldAnuncio = anuncio
    teste = oldAnuncio.imgPath.url.replace("/", "\\")
    # print(teste)
    imgPath = os.getcwd()+teste
    if(os.path.isfile(imgPath)):
        os.remove(imgPath)
    #O nome da variavel tem q ser o msm do atributo (neste caso pk = pk) não sei porque
    if request.method == 'POST':

        #inicia o form com o que o usuario passou ou com o que foi buscado do banco de dados
        form = AnuncioForm(request.POST or None, request.FILES, instance=anuncio)
        form.fields['usuario'].initial = anuncio.usuario

        #valida o form
        if form.is_valid():
            form.save()
            #Redirect para o metodo minha_conta sem duplicar dados de cadastro e na url certa
            return redirect('url_minha_conta')

    dados['form'] = AnuncioForm(instance=anuncio)
    dados['usuario'] = request.user
    dados['titulo'] = "Atualizar Anúncio"
    return render(request, 'loja/form.html', dados)

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def excluir_anuncio(request, pk):
    dados = {}
    #O nome da variavel tem q ser o msm do atributo (neste caso pk = pk) não sei porque
    anuncio = Anuncio.objects.get(pk = pk)
    anuncio.delete()
    #Redirect para o metodo minha_conta sem duplicar dados de cadastro e na url certa
    return redirect('url_minha_conta')

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def detalhes_anuncio(request, pk):
    #select * from Anuncio
    dados = {}
    dados['anuncios'] = Anuncio.objects.filter(pk = pk)
    dados['categorias'] = Categoria.objects.all()
    dados['usuario'] = request.user
    return render(request, 'loja/detalhes_anuncio.html', dados)

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def listar_por_categoria(request, pk):
    dados = {}
    dados['anuncios'] = Anuncio.objects.filter(categoria = pk)
    dados['categorias'] = Categoria.objects.all()
    dados['usuario'] = request.user
    #print(dados['anuncios'].query) #Exibe no terminal
    return render(request, 'loja/home.html', dados)

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def pesquisa_filtrada(request):
    dados = {}
    if request.POST:
        chave = request.POST.get('chave')
        #Pesquisa por um padrao especifico no titulo == like do SQL
        dados['anuncios'] = Anuncio.objects.filter(titulo__contains=chave)
        dados['categorias'] = Categoria.objects.all()
        dados['usuario'] = request.user
        #print(dados['anuncios'].query) #Exibe no terminal
        return render(request, 'loja/home.html', dados)

    return redirect(home(request))

#-----------------------------------------------------------------------------------------
#Quando nao usar @login_required e a sua pagina usar um csrf token vc deve usar csrf_protect no metodo que chama aquele form html
@csrf_protect
def cadastrar_usuario(request):
    
    dados = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()
            print('Cadastrado ocom sucesso')
            return render(request, 'loja/login.html')
    else:
        print('Metodo de envio nao eh POST')
        form = RegistrationForm()        
        dados['usuario'] =  form
        return render(request, 'loja/form_usuario.html', dados)


#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def menu(request):
    return render(request, 'loja/menu.html')

#-----------------------------------------------------------------------------------------
@login_required(login_url='url_index')
def pagamento(request):
    return render(request, 'loja/pagamento.html')