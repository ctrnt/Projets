from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='base'),
    path('article/<path:doi>/', views.page_article, name='page_article'), #PAGE ARTICLE
    path('auteur/<path:prenom>/<path:nom>/', views.page_auteur, name='page_auteur'), #PAGE AUTEUR
    path('labo/<path:nom_labo>', views.page_labo, name='page_labo'), #PAGE LABO
    path('pays/<path:pays>', views.page_pays, name='page_pays'), #PAGE PAYS
    path('journal/<path:journal>', views.page_journal, name='page_journal'), #PAGE JOURNAL
    path('SearchBar', views.SearchBar, name='SearchBar'), #SearchBar
    path('AuthorSearch', views.AuthorSearch, name='AuthorSearch'), #AuthorSearch
    path('LabSearch', views.LabSearch, name='LabSearch'), #LabSearch
    path('PaysSearch', views.PaysSearch, name='PaysSearch'), #PaysSearch
    path('ThemeSearch', views.ThemeSearch, name='ThemeSearch'), #ThemeSearch
    path('DateSearch', views.DateSearchInit, name='DateSearch'), #DateSearch
    path('JournalSearch', views.JournalSearch, name='JournalSearch'), #JournalSearch
    path('TypeSearch', views.TypeSearch, name='TypeSearch'), #TypeSearch
]
