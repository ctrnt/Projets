from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import *
import time
import datetime as dt
from itertools import chain
import matplotlib.pyplot as plt
import pandas as pd
import os

def home(request):
    return render(request, 'home.html')

#=================================================================================================================================

def page_article(request, doi):
    article = Article.objects.get(doi=doi)
    types = Type.objects.filter(types_article__article_id=article)
    themes = Theme.objects.filter(sous_theme__sous_themes_article__article_id=article)
    sous_themes = Sous_Theme.objects.filter(sous_themes_article__article_id=article)
    auteurs = Auteur.objects.filter(auteurs_article__article_id=article)
    labos = Labo.objects.filter(labos_article__article_id=article)
    
    count=['','','','','']
    if len(types)==1:
        count[0] = 'Type :'
    if len(types)!=0:
        count[0] = 'Types :'
    if len(themes)==1:
        count[1] = 'Theme :'
    if len(themes)!=0:
        count[1] = 'Themes :'
    if len(sous_themes)==1:
        count[2] = 'Sous-Theme :'
    if len(sous_themes)!=0:
        count[2] = 'Sous-Themes :'
    if len(auteurs)==1:
        count[3] = 'Auteur :'
    elif len(auteurs)>1:
        count[3] = 'Auteurs (' + str(len(auteurs)) + ') :'
    if len(labos)==1:
        count[4] = 'Labo :'
    elif len(labos)>1:
        count[4] = 'Labos (' + str(len(labos)) + ') :'
    
    context = {
        'article':article,
        'auteurs':auteurs,
        'labos':labos,
        'types':types,
        'themes':themes,
        'sous_themes':sous_themes,
        'count':count
    }
    return render(request, 'page_article.html', context)

#=================================================================================================================================

def page_auteur(request, prenom, nom):
    auteur = Auteur.objects.get(prenom=prenom, nom=nom)
    articles = Article.objects.filter(auteurs_article__auteur_id=auteur)
    labos = Labo.objects.filter(labos_auteur__auteur_id=auteur)
    lmail=str(auteur.email).split(',')
    email_list = [email.replace('{', '').replace('}', '') for email in lmail]

    count=['','']
    if len(articles)==1:
        count[0] = 'Article :'
    elif len(articles)>1:
        count[0] = 'Articles (' + str(len(articles)) + ') :'
    if len(labos)==1:
        count[1] = 'Labo :'
    elif len(labos)>1:
        count[1] = 'Labos (' + str(len(labos)) + ') :'

    context = {
        'auteur':auteur,
        'email_list':email_list,
        'articles':articles,
        'labos':labos,
        "count":count
    }
    return render(request, 'page_auteur.html', context)

#=================================================================================================================================

def page_labo(request, nom_labo):
    labo = Labo.objects.get(laboratoire=nom_labo)
    articles = Article.objects.filter(labos_article__labo_id=labo)
    auteurs = Auteur.objects.filter(labos_auteur__labo_id=labo)
    pays = Pays.objects.filter(labos_pays__labo_id=labo)

    count=['','','']
    if len(articles)==1:
        count[0] = 'Article :'
    elif len(articles)>1:
        count[0] = 'Articles (' + str(len(articles)) + ') :'
    if len(auteurs)==1:
        count[1] = 'Auteur :'
    elif len(auteurs)>1:
        count[1] = 'Auteurs (' + str(len(auteurs)) + ') :'
    if len(pays)==1:
        count[2] = 'Pays :'
    else:
        count[2] = 'Pays (' + str(len(pays)) + ') :'

    context = {
        'labo': labo,
        'articles': articles,
        'auteurs': auteurs,
        'pays':pays,
        "count":count
    }
    return render(request, 'page_labo.html', context)

#=================================================================================================================================

def page_pays(request, pays):
    pays = Pays.objects.get(pays=pays)
    labos = Labo.objects.filter(labos_pays__pays_id=pays)
    
    if len(labos)==1:
        count = "Labo :"
    else:
        count = 'Labos (' + str(len(labos)) + ') :'

    context = {
        'pays':pays,
        'labos':labos,
        'count':count
    }
    return render(request, 'page_pays.html', context)

#=================================================================================================================================

def page_journal(request, journal):
    journal = Journal.objects.get(nom_journal=journal)
    articles = Article.objects.filter(journal_id=journal)

    if len(articles)==1:
        count = "Article :"
    else:
        count = 'Articles (' + str(len(articles)) + ') :'

    context = {
        'journal':journal,
        'articles':articles,
        'count':count
    }
    return render(request, 'page_journal.html', context)

#=================================================================================================================================

def SearchBar(request):
    recherche_raw = request.GET.get('recherche')
    choix = request.GET.get('choix')

    if choix=='titre' and recherche_raw:
        recherche = recherche_raw.split(' ')

        debut = time.time()
        titres = Article.objects.filter(titre__icontains=recherche[0])
        for mot_clé in recherche[1:]:
            titres = titres.filter(titre__icontains=mot_clé)
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'
        
        if len(titres)==0:
            count = f"Aucun article trouvé pour '{recherche_raw}'"
            temps=''
        elif len(titres)==1:
            count = f"1 article trouvé pour '{recherche_raw}'"
        else:
            count = f"{str(len(titres))} articles trouvés pour '{recherche_raw}'"
        
        context = {
            'titres':titres,
            'count':count,
            'temps':temps
        }
        return render(request, 'SearchBar.html', context)

    if choix=='doi' and recherche_raw:
        debut = time.time()
        try:
            article = get_object_or_404(Article, doi=recherche_raw)
        except Http404:
            count = f"Aucun article trouvé pour '{recherche_raw}'"
            context = {
                'count':count,
            }
            return render(request, 'SearchBar.html', context)
        
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'
        count = f"1 article trouvé pour '{recherche_raw}'"
        context = {
            'article':article,
            'count':count,
            'temps':temps
        }
        return render(request, 'SearchBar.html', context)
    return render(request, 'SearchBar.html')

#=================================================================================================================================

def AuthorSearch(request):
    prenom = request.GET.get('prenom')
    nom = request.GET.get('nom')
    
    if not prenom and not nom:
        return render(request, 'AuthorSearch.html')
    
    if prenom and nom:
        debut = time.time()
        try:
            auteur = get_object_or_404(Auteur, prenom=prenom, nom=nom)
        except Http404:
            count = f"Aucun auteur trouvé pour '{prenom} , {nom}'"
            context = {
                'count':count,
            }
            return render(request, 'AuthorSearch.html', context)
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'
        count = f"1 auteur trouvé pour '{prenom} , {nom}'"
        context = {
            'auteur':auteur,
            'count':count,
            'temps':temps
        }
        print(auteur)
        return render(request, 'AuthorSearch.html', context)   
        
    elif prenom:
        debut = time.time()
        auteurs = Auteur.objects.filter(prenom=prenom)
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'
        if len(auteurs)==0:
            count = f"Aucun auteur trouvé pour {prenom}"
        elif len(auteurs)==1:
            count = f"1 auteur trouvé pour '{prenom}'"
        else:
            count = f"{len(auteurs)} auteurs trouvés pour '{prenom}'"
        context = {
            'auteurs':auteurs,
            'count':count,
            'temps':temps
        }
        return render(request, 'AuthorSearch.html', context)
    
    elif nom:
        debut = time.time()
        auteurs = Auteur.objects.filter(nom=nom)
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'
        if len(auteurs)==0:
            count = f"Aucun auteur trouvé pour {nom}"
        elif len(auteurs)==1:
            count = f"1 auteur trouvé pour '{nom}'"
        else:
            count = f"{len(auteurs)} auteurs trouvés pour '{nom}'"
        context = {
            'auteurs':auteurs,
            'count':count,
            'temps':temps
        }
        return render(request, 'AuthorSearch.html', context)
    
    return render(request, 'AuthorSearch.html')

#=================================================================================================================================

def LabSearch(request):
    recherche_raw = request.GET.get('recherche')
    if recherche_raw:
        recherche=recherche_raw.split(' ')

        debut = time.time()
        labos = Labo.objects.filter(laboratoire__icontains=recherche[0])
        for mot in recherche[1:]:
            labos = labos.filter(laboratoire__icontains=mot)
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'

        if len(labos)==0:
            count = f"Aucun labo trouvé pour '{recherche_raw}'"
            temps=''
        elif len(labos)==1:
            count = f"1 labo trouvé pour '{recherche_raw}'"
        else:
            count = f"{str(len(labos))} labos trouvés pour '{recherche_raw}'"

        context = {
            'labos':labos,
            'count':count,
            'temps':temps
        }
        return render(request, 'LabSearch.html', context)
    
    else:
        return render(request, 'LabSearch.html')

#=================================================================================================================================

def PaysSearch(request):
    AllPays = Pays.objects.all()
    context = {
        'AllPays':AllPays
    }
    return render(request, 'PaysSearch.html', context)

#=================================================================================================================================

def ThemeSearch(request):
    AllThemes = Theme.objects.all()
    AllSous_Themes = Sous_Theme.objects.all()
    recherche_theme = request.GET.get('theme')
    recherche_sous_theme = request.GET.get('sous_theme')
    recherche_titre_raw = request.GET.get('titre')
    context = {
        'AllThemes':AllThemes,
        'AllSous_Themes':AllSous_Themes,
    }
    if recherche_theme and recherche_sous_theme:
        theme = Theme.objects.get(nom_theme=recherche_theme)
        sous_theme = Sous_Theme.objects.get(nom_sous_theme=recherche_sous_theme)

        debut=time.time()
        articles = Article.objects.filter(sous_themes_article__sous_theme_id=sous_theme)

        if recherche_titre_raw:
            recherche_titre = recherche_titre_raw.split(' ')
            for mot_clé in recherche_titre:
                articles = articles.filter(titre__icontains=mot_clé)
        temps = '(' + str(round(time.time()-debut, 2)) + 's)'
        if len(articles)==0:
            count = f"Aucun article trouvé pour '{sous_theme}' , '{recherche_titre_raw}'"
        elif len(articles)==1:
            count = f"1 article trouvé pour '{sous_theme}' , '{recherche_titre_raw}'"
        elif len(articles)>1:
            count = f"{len(articles)} articles trouvés pour '{sous_theme}' , '{recherche_titre_raw}'"

        context = {
        'AllThemes':AllThemes,
        'AllSous_Themes':AllSous_Themes,
        'articles':articles,
        'count':count,
        'temps':temps
        }
        return render(request, 'ThemeSearch.html', context)
    return render(request, 'ThemeSearch.html', context)

#=================================================================================================================================

def DateSearchInit(request):
    histo = 'website/static/barchart.png'
    if os.path.isfile(histo):
        os.remove(histo)
    debut = request.GET.get('debut')
    fin = request.GET.get('fin')
    choix = request.GET.get('choix')
    choix_hist = request.GET.get('choix_hist')
    titre_raw = request.GET.get('titre')

    if debut and fin:
        debut = dt.datetime.strptime(debut, '%Y-%m-%d').date()
        fin = dt.datetime.strptime(fin, '%Y-%m-%d').date()
        debut_time = time.time()

        if choix!='histogramme':
            if choix == 'date_exacte':
                delta = fin.year-debut.year
                annees_a_couvrir = []
                articles_fd = Article_Fulldate.objects.filter(date__range=[debut,fin])
                articles_y = []

                if delta>=2:
                    for i in range(1,delta):
                        annees_a_couvrir.append(debut.year+i)
                    annees_a_couvrir = [annees_a_couvrir[0], annees_a_couvrir[-1]]
                    articles_y = Article_Year.objects.filter(date__range=annees_a_couvrir)

            elif choix =='année':
                articles_fd = Article_Fulldate.objects.filter(date__year__range=[debut.year,fin.year])
                articles_y = Article_Year.objects.filter(date__range=[debut.year,fin.year])

            if titre_raw:
                Ltitre = titre_raw.split(' ')
                for mot_clé in Ltitre:
                    articles_fd = articles_fd.filter(titre__icontains=mot_clé)
                    articles_y = articles_y.filter(titre__icontains=mot_clé)

                articles = list(chain(articles_fd, articles_y))
                temps = '(' + str(round(time.time()-debut_time, 2)) + 's)'

                if choix == 'date_exacte':
                    if len(articles)==0:
                        count = f"Aucun article publié entre le '{debut}' et le '{fin}' avec '{titre_raw}'"
                    elif len(articles)==1:
                        count = f"1 article publié entre le '{debut}' et le '{fin}' avec '{titre_raw}'"
                    elif len(articles)>1:
                        count = f"{len(articles)} articles publiés entre le '{debut}' et le '{fin}' avec '{titre_raw}'"

                elif choix == 'année':
                    if fin.year-debut.year==0:
                        if len(articles)==0:
                            count = f"Aucun article publié en '{debut.year}' avec '{titre_raw}'"
                        elif len(articles)==1:
                            count = f"1 article publié en '{debut.year}' avec '{titre_raw}'"
                        elif len(articles)>1:
                            count = f"{len(articles)} articles publiés en '{debut.year}' avec '{titre_raw}'"
                    else:
                        if len(articles)==0:
                            count = f"Aucun article publié entre '{debut.year}' et '{fin.year}' avec '{titre_raw}'"
                        elif len(articles)==1:
                            count = f"1 article publié entre '{debut.year}' et '{fin.year}' avec '{titre_raw}'"
                        elif len(articles)>1:
                            count = f"{len(articles)} articles publiés entre '{debut.year}' et '{fin.year}' avec '{titre_raw}'"
            
                context = {
                    'articles':articles,
                    'count':count,
                    'temps':temps                
                }
                return render(request, 'DateSearch.html', context)
            
            articles = list(chain(articles_fd, articles_y))
            temps = '(' + str(round(time.time()-debut_time, 2)) + 's)'

            if choix == 'date_exacte':
                    if len(articles)==0:
                        count = f"Aucun article publié entre le '{debut}' et le '{fin}'"
                    elif len(articles)==1:
                        count = f"1 article publié entre le '{debut}' et le '{fin}'"
                    elif len(articles)>1:
                        count = f"{len(articles)} articles publiés entre le '{debut}' et le '{fin}'"

            elif choix == 'année':
                if fin.year-debut.year==0:
                    if len(articles)==0:
                        count = f"Aucun article publié en '{debut.year}'"
                    elif len(articles)==1:
                        count = f"1 article publié en '{debut.year}'"
                    elif len(articles)>1:
                        count = f"{len(articles)} articles publiés en '{debut.year}'"
                else:
                    if len(articles)==0:
                        count = f"Aucun article publié entre '{debut.year}' et '{fin.year}'"
                    elif len(articles)==1:
                        count = f"1 article publié entre '{debut.year}' et '{fin.year}'"
                    elif len(articles)>1:
                        count = f"{len(articles)} articles publiés entre '{debut.year}' et '{fin.year}'"

            context = {
                'articles':articles,
                'count':count,
                'temps':temps
            }
            return render(request, 'DateSearch.html', context)
        
        if choix == 'histogramme':
            if choix_hist == 'jour':
                delta = fin - debut
                articles_par_jour = []
                les_jours_en_str = []

                for i in range(delta.days + 1):
                    day = debut + dt.timedelta(days=i)
                    articles = Article_Fulldate.objects.filter(date=day)
                    articles_par_jour.append(len(articles))
                    les_jours_en_str.append(str(day))

                les_jours_courts = [jour[-5:] for jour in les_jours_en_str]
                plt.bar(les_jours_en_str, articles_par_jour)
                plt.xticks(range(0, len(les_jours_en_str), 60), les_jours_courts[::60])
                plt.title(f"Articles par jour du {debut} au {fin}")
                plt.savefig('website/static/barchart.png')
                plt.clf()

                return render(request, 'DateSearch.html')
            
            elif choix_hist == 'semaine':
                articles_par_jour = []
                les_jours_en_str = []
                periode_tps = pd.period_range(debut, fin, freq='w')
                date_debut = (str(periode_tps[0]).split('/'))[0]
                date_fin = (str(periode_tps[-1]).split('/'))[-1]
                week_count = 1
                for i in periode_tps:
                    week_split = str(i).split('/')
                    debut_semaine = dt.datetime.strptime(week_split[0], '%Y-%m-%d').date()
                    fin_semaine = dt.datetime.strptime(week_split[1], '%Y-%m-%d').date()
                    articles_par_jour.append(len(Article_Fulldate.objects.filter(date__range=[debut_semaine,fin_semaine])))
                    les_jours_en_str.append(str(week_count))
                    week_count+=1
                plt.bar(les_jours_en_str, articles_par_jour)
                if len(les_jours_en_str)>=23:
                    plt.xticks(range(0, len(les_jours_en_str), 3), les_jours_en_str[::3])
                plt.title(f"Articles par semaine du {date_debut} au {date_fin}")
                plt.savefig('website/static/barchart.png')
                plt.clf()
                return render(request, 'DateSearch.html')

            elif choix_hist == 'mois':
                articles_par_jour = []
                les_jours_en_str = []
                periode_tps = pd.period_range(debut, fin, freq='M') 
                for date in periode_tps:
                    articles_par_jour.append(len(Article_Fulldate.objects.filter(date__year=date.year,date__month=date.month)))
                    les_jours_en_str.append(f'{date.year}-{date.month}')
                plt.bar(les_jours_en_str, articles_par_jour)
                plt.title(f"Articles par mois de {debut.month}/{debut.year} à {fin.month}/{fin.year}")
                plt.savefig('website/static/barchart.png')
                plt.clf()
                return render(request, 'DateSearch.html')
            
            elif choix_hist == 'année':
                articles_par_jour = []
                les_jours_en_str = []
                for annee in range(debut.year, fin.year+1):
                    nb_articles = len(Article_Fulldate.objects.filter(date__year=annee)) + len(Article_Year.objects.filter(date=annee))
                    articles_par_jour.append(nb_articles)
                    les_jours_en_str.append(str(annee))

                les_jours_courts = [jour[-2:] for jour in les_jours_en_str]
                plt.bar(les_jours_en_str, articles_par_jour)
                plt.xticks(range(0, len(les_jours_en_str), 2), les_jours_courts[::2])
                if len(range(debut.year, fin.year+1))==1:
                    plt.title(f"Articles en {debut.year}")
                else:
                    plt.title(f"Articles par année de {debut.year} à {fin.year}")
                plt.savefig('website/static/barchart.png')
                plt.clf()

                compteur=0
                for nb in articles_par_jour:
                    compteur+=nb
                print(compteur)
                return render(request, 'DateSearch.html')
    else :
        return render(request, 'DateSearch.html')

#=================================================================================================================================

def JournalSearch(request):
    recherche_raw = request.GET.get('recherche')
    if recherche_raw:
        recherche = recherche_raw.split(' ')
        debut=time.time()
        journaux = Journal.objects.filter(nom_journal__icontains=recherche[0])
        for mot_clé in recherche[1:]:
            journaux = journaux.filter(nom_journal__icontains=mot_clé)

        temps = '(' + str(round(time.time()-debut, 2)) + 's)'

        if len(journaux)==0:
                count = f"Aucun journal trouvé pour '{recherche_raw}'"
                temps=''
        elif len(journaux)==1:
            count = f"1 journal trouvé pour '{recherche_raw}'"
        else:
            count = f"{str(len(journaux))} journaux trouvés pour '{recherche_raw}'"

        context = {
            'journaux':journaux,
            'count':count,
            'temps':temps
        }
        return render(request, 'JournalSearch.html', context)
    return render(request, 'JournalSearch.html')

#=================================================================================================================================

def TypeSearch(request):
    AllTypes = Type.objects.all()
    recherche = request.GET.get('recherche')
    context = {
                'AllTypes':AllTypes,
            }
    
    if recherche:
        type = Type.objects.get(nom_type=recherche)
        articles = Article.objects.filter(types_article__type_id=type)
        dico = {}
        for article in articles:
            if str(article.journal_id) in dico:
                dico[str(article.journal_id)]+=1
            else:
                dico[str(article.journal_id)]=1

        dico_decroissant = dict(sorted(dico.items(), key=lambda item: item[1], reverse=True))

        journaux=list(dico_decroissant.keys())
        valeurs=list(dico_decroissant.values())

        liste=[]
        for i in range(len(journaux)):
            liste.append(journaux[i]+' | '+str(valeurs[i])+' articles')
        context = {
            'AllTypes':AllTypes,
            'type':type,
            'liste':liste
        }
        return render(request, 'TypeSearch.html', context)
    
    return render(request, 'TypeSearch.html', context)

#=================================================================================================================================


        