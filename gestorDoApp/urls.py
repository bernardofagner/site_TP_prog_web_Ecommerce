"""gestorDoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings
from django.urls import path
from loja.views import (login_user, pagamento, index, logout_user, minha_conta, home,
                        cadastrar_anuncio, menu, atualizar_anuncio, excluir_anuncio,
                        cadastrar_usuario, listar_por_categoria, pesquisa_filtrada, detalhes_anuncio
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='url_index'),
    path('login_user/', login_user, name='url_login_user'),
    path('logout/', logout_user, name='url_logout_user'),
    path('menu/', menu, name='url_menu'),
    path('home/', home, name='url_home'),

    path('pagamento/', pagamento),
    path('minha_conta/', minha_conta, name='url_minha_conta'),

    path('cadastrar/', cadastrar_anuncio, name='url_cadastrar_anuncio'),
    path('atualizar/<int:pk>', atualizar_anuncio, name='url_atualizar_anuncio'),
    path('excluir/<int:pk>', excluir_anuncio, name='url_excluir_anuncio'),
    path('detalhes/<int:pk>', detalhes_anuncio, name='url_detalhes_anuncio'),

    path('listar_por_categoria/<int:pk>', listar_por_categoria, name='url_listar_por_categoria'),
    path('pesquisa_filtrada', pesquisa_filtrada, name='url_pesquisa_filtrada'),

    path('cadastrar_usuario', cadastrar_usuario, name='cadastrar_usuario')
]

#Configuracoes para poder fazer uplaod de imagens
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)