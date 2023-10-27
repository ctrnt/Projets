import os, shutil, zipfile, psycopg2
import pandas as pd
from ART_JOUR import articles_journaux
from THEMES_TYPES import themes_ssthemes_types
from TRAITEMENT_JSON import filedotjson
from CSVAUTEURS import auteursetcie
from AUTEURS_LABOS import auteurs_labos_pays

#on unzip le dossier archive
zip=zipfile.ZipFile('archive.zip')
zip.extractall()

#on stocke le path du répertoire source
path_source = os.getcwd()

#on supprime le dossier inutile '0_table_formats_and_column_definitions'
shutil.rmtree(path_source+'//archive//Kaggle//target_tables//0_table_formats_and_column_definitions')

#on supprime le dossier inutile 'unsorted_tables'
shutil.rmtree(path_source+'//archive//Kaggle//target_tables//unsorted_tables')

########################################################################################################################################################################################################################

#on ouvre le metadata.csv
metadata=pd.read_csv(path_source+'//archive//metadata.csv',sep=',',low_memory=False)

#on execute la fonction articles_journaux
metadata_v2, listepmcid, listepubmed, doi_ARTICLE, titre_ARTICLE, date_ARTICLE, lien_ARTICLE, nom_journal_JOURNAL, journal_id_ARTICLE, doi_ART_FULL, titre_ART_FULL, date_ART_FULL, doi_ART_YEAR, titre_ART_YEAR, date_ART_YEAR = articles_journaux(metadata)

#on execute la fonction themes_ssthemes_types
nom_theme_THEME, nom_sous_theme_SSTHEME, sstheme_id_SSTHEMESARTICLE, article_id_SSTHEMESARTICLE, theme_id_SSTHEME, nom_type_TYPE, type_id_TYPESARTICLE, article_id_TYPESARTICLE = themes_ssthemes_types(doi_ARTICLE, listepmcid, listepubmed)

#on execute la fonction auteursetcie
auteurs_csv = auteursetcie(metadata_v2, doi_ARTICLE)

#on execute la fonction auteurs_labos_pays
prenom_AUTEUR, nom_AUTEUR, email_AUTEUR, auteur_id_AUT_ART, article_id_AUT_ART, labo_id_LAB_AUT, auteur_id_LAB_AUT, laboratoire_LABO, labo_id_LAB_ART, article_id_LAB_ART, pays_PAYS, labo_id_LAB_PAYS, pays_id_LAB_PAYS = auteurs_labos_pays(auteurs_csv, doi_ARTICLE)

########################################################################################################################################################################################################################

conn = psycopg2.connect(
    host='localhost',
    database='DBCOVID',
    user='postgres',
    password='dbpasswd'
)
cur = conn.cursor()

#TABLE PAYS
for i in range(len(pays_PAYS)):
    cur.execute("INSERT INTO website_pays (pays) VALUES (%s)", (pays_PAYS[i],))
print('TABLE PAYS done')

#TABLE LABO
for i in range(len(laboratoire_LABO)):
    cur.execute("INSERT INTO website_labo (laboratoire) VALUES (%s)", (laboratoire_LABO[i],))
print('TABLE LABO done')

#TABLE JOURNAL
for i in range(len(nom_journal_JOURNAL)):
    cur.execute("INSERT INTO website_journal (nom_journal) VALUES (%s)", (nom_journal_JOURNAL[i],))
print('TABLE JOURNAL done')

#TABLE TYPE
for i in range(len(nom_type_TYPE)):
    cur.execute("INSERT INTO website_type (nom_type) VALUES (%s)", (nom_type_TYPE[i],))
print('TABLE TYPE done')

#TABLE THEME
for i in range(len(nom_theme_THEME)):
    cur.execute("INSERT INTO website_theme (nom_theme) VALUES (%s)", (nom_theme_THEME[i],))
print('TABLE THEME done')

#TABLE SOUS_THEME
for i in range(len(nom_sous_theme_SSTHEME)):
    cur.execute("INSERT INTO website_sous_theme (nom_sous_theme, theme_id) VALUES (%s, %s)", (nom_sous_theme_SSTHEME[i],theme_id_SSTHEME[i],))
print('TABLE SOUS_THEME done')

#TABLE ARTICLE
for i in range(len(doi_ARTICLE)):
    cur.execute("INSERT INTO website_article (doi, titre, date, lien, journal_id) VALUES (%s, %s, %s, %s, %s)", (doi_ARTICLE[i], titre_ARTICLE[i], date_ARTICLE[i], lien_ARTICLE[i], journal_id_ARTICLE[i],))
print('TABLE ARTICLE done')

#TABLE TYPES_ARTICLE
for i in range(len(article_id_TYPESARTICLE)):
    cur.execute("INSERT INTO website_types_article (article_id, type_id) VALUES (%s, %s)", (article_id_TYPESARTICLE[i], type_id_TYPESARTICLE[i],))
print('TABLE TYPES_ARTICLE done')

#TABLE SOUS_THEMES_ARTICLE
for i in range(len(article_id_SSTHEMESARTICLE)):
    cur.execute("INSERT INTO website_sous_themes_article (article_id, sous_theme_id) VALUES (%s, %s)", (article_id_SSTHEMESARTICLE[i], sstheme_id_SSTHEMESARTICLE[i],))
print('TABLE SOUS_THEMES_ARTICLE done')

#TABLE AUTEUR
for i in range(len(nom_AUTEUR)):
    cur.execute("INSERT INTO website_auteur (nom, prenom, email) VALUES (%s, %s, %s)", (nom_AUTEUR[i], prenom_AUTEUR[i], email_AUTEUR[i],))
print('TABLE AUTEUR done')

#TABLE AUTEURS_ARTICLE
for i in range(len(article_id_AUT_ART)):
    cur.execute("INSERT INTO website_auteurs_article (article_id, auteur_id) VALUES (%s, %s)", (article_id_AUT_ART[i], auteur_id_AUT_ART[i],))
print('TABLE AUTEURS_ARTICLE done')

#TABLE LABOS_AUTEUR
for i in range(len(labo_id_LAB_AUT)):
    cur.execute("INSERT INTO website_labos_auteur (labo_id, auteur_id) VALUES (%s, %s)", (labo_id_LAB_AUT[i], auteur_id_LAB_AUT[i],))
print('TABLE LABOS_AUTEUR done')

#TABLE LABOS_ARTICLE
for i in range(len(labo_id_LAB_ART)):
    cur.execute("INSERT INTO website_labos_article (labo_id, article_id) VALUES (%s, %s)", (labo_id_LAB_ART[i], article_id_LAB_ART[i],))
print('TABLE LABOS_ARTICLE done')

#TABLE LABOS_PAYS
for i in range(len(labo_id_LAB_PAYS)):
    cur.execute("INSERT INTO website_labos_pays (labo_id, pays_id) VALUES (%s, %s)", (labo_id_LAB_PAYS[i], pays_id_LAB_PAYS[i],))
print('TABLE LABOS_PAYS done')

#TABLE ARTICLE_FULLDATE
for i in range(len(doi_ART_FULL)):
    cur.execute("INSERT INTO website_article_fulldate (doi, titre, date) VALUES (%s, %s, %s)", (doi_ART_FULL[i], titre_ART_FULL[i], date_ART_FULL[i],))
print('TABLE ARTICLE_FULLDATE done')

#TABLE ARTICLE_YEAR
for i in range(len(doi_ART_YEAR)):
    cur.execute("INSERT INTO website_article_year (doi, titre, date) VALUES (%s, %s, %s)", (doi_ART_YEAR[i], titre_ART_YEAR[i], date_ART_YEAR[i],))
print('TABLE ARTICLE_YEAR done')

conn.commit()
cur.close()
conn.close()
