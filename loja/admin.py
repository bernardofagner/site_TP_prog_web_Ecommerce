from django.contrib import admin
from .models import Anuncio
#from .models import Usuario
from .models import Compra
from .models import Categoria

# Register your models here, them will apear in the admin view in the website
admin.site.register(Anuncio)
#admin.site.register(Usuario)
admin.site.register(Compra)
admin.site.register(Categoria)