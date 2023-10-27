from django.db import models
    
class Pays(models.Model):
    pays_id = models.AutoField(primary_key=True)
    pays = models.TextField(null=True)

    def __str__(self):
        return self.pays
    
class Labo(models.Model):
    labo_id = models.AutoField(primary_key=True)
    laboratoire = models.TextField(null=True)

    def __str__(self):
        return self.laboratoire

class Journal(models.Model):
    journal_id = models.AutoField(primary_key=True)
    nom_journal = models.TextField(null=True)

    def __str__(self):
        return self.nom_journal

class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    nom_type = models.TextField(null=True)

    def __str__(self):
        return self.nom_type

class Theme(models.Model):
    theme_id = models.AutoField(primary_key=True)
    nom_theme = models.TextField(null=True)

    def __str__(self):
        return self.nom_theme 

class Sous_Theme(models.Model):
    sous_theme_id = models.AutoField(primary_key=True)
    nom_sous_theme = models.TextField(null=True)
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id', null=True)

    def __str__(self):
        return self.nom_sous_theme

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    doi = models.TextField(null=True)
    titre = models.TextField(null=True)
    date = models.TextField(null=True)
    lien = models.URLField(max_length = 250, null=True)
    journal_id = models.ForeignKey(Journal, on_delete=models.CASCADE, db_column='journal_id', null=True)

    def __str__(self):
        return self.doi

class Types_Article(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, db_column='article_id', null=True)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE, db_column='type_id', null=True)

    def __str__(self):
        return f"{self.article_id} {self.type_id}"

class Sous_Themes_Article(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, db_column='article_id', null=True)
    sous_theme_id = models.ForeignKey(Sous_Theme, on_delete=models.CASCADE, db_column='sous_theme_id', null=True)

    def __str__(self):
        return f"{self.article_id} {self.sous_theme_id}"
    
class Auteur(models.Model):
    auteur_id = models.AutoField(primary_key=True)
    nom = models.TextField(null=True)
    prenom = models.TextField(null=True)
    email = models.TextField(null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Auteurs_Article(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, db_column='article_id', null=True)
    auteur_id = models.ForeignKey(Auteur, on_delete=models.CASCADE, db_column='auteur_id', null=True)

    def __str__(self):
        return f"{self.article_id} {self.auteur_id}"    

class Labos_Auteur(models.Model):
    labo_id = models.ForeignKey(Labo, on_delete=models.CASCADE, db_column='labo_id', null=True)
    auteur_id = models.ForeignKey(Auteur, on_delete=models.CASCADE, db_column='auteur_id', null=True)

    def __str__(self):
        return f"{self.labo_id} {self.auteur_id}"
        
class Labos_Article(models.Model):
    labo_id = models.ForeignKey(Labo, on_delete=models.CASCADE, db_column='labo_id', null=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, db_column='article_id', null=True)

    def __str__(self):
        return f"{self.article_id} {self.labo_id}"

class Labos_Pays(models.Model):
    labo_id = models.ForeignKey(Labo, on_delete=models.CASCADE, db_column='labo_id', null=True)
    pays_id = models.ForeignKey(Pays, on_delete=models.CASCADE, db_column='pays_id', null=True)

    def __str__(self):
        return f"{self.labo_id} {self.pays_id}"
    
class Article_Fulldate(models.Model):
    doi = models.TextField(null=True)
    titre = models.TextField(null=True)
    date = models.DateField(null=True)

class Article_Year(models.Model):
    doi = models.TextField(null=True)
    titre = models.TextField(null=True)
    date = models.IntegerField(null=True)