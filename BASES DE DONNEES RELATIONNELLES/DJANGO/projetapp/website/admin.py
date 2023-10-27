from django.contrib import admin
from .models import *

admin.site.register(Article_Fulldate)
admin.site.register(Article_Year)

admin.site.register(Labo)
admin.site.register(Journal)
admin.site.register(Type)
admin.site.register(Theme)
admin.site.register(Sous_Theme)
admin.site.register(Article)

admin.site.register(Sous_Themes_Article)
admin.site.register(Types_Article)

admin.site.register(Auteur)
admin.site.register(Auteurs_Article)
admin.site.register(Labos_Auteur)
admin.site.register(Labos_Article)