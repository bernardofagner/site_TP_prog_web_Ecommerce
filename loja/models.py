from django.db import models
from django.contrib.auth.models import User #Importa a tabela de usuarios do Django
from django.conf import settings

#-----------------------------------------------------------------------------------------
#Se nao criarmos o campo PrimaryKey o Django vai cria-lo automaticamente
#-----------------------------------------------------------------------------------------
#Define as categorias que os anuncios podem ter
class Categoria(models.Model):
    nome = models.CharField(max_length=20)
    imgPath = models.ImageField(null=True, upload_to='img/category')

    #Define como retornar o valor de cada atributo da classe
    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        self.imgPath.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categorias'

#-----------------------------------------------------------------------------------------
#Guarda todos os anuncios cadastrados no banco de dados
class Anuncio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    imgPath = models.ImageField(null=True, upload_to='img/', default='', blank=True)
    #Relacionamento 1 para 1 em OneToOneField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)


    #Define como retornar o valor de cada atributo da classe
    def __str__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        self.imgPath.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Anuncios'

#-----------------------------------------------------------------------------------------
#Lida com a especificacao da tabela compra
class Compra(models.Model):
    produto = models.ForeignKey(Anuncio, on_delete=models.CASCADE, null=True)
    #comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    qtd = models.IntegerField()
    valor = models.DecimalField(max_digits=7, decimal_places=2)
    dt_compra = models.DateTimeField(auto_now_add=True)

    #Define como retornar o valor de cada atributo da classe
    def __str__(self):
        return self.produto.titulo

    class meta:
        verbose_name_plural = 'Compras'
    

