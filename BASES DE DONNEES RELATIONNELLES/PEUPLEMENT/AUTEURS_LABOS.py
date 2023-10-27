import pandas as pd

def auteurs_labos_pays(df, listedoi):

    auteurs2 = df.groupby(['prenom','nom']).agg({
        'doi': lambda x: list(set(x)),
        'email': lambda x: list(set(x)), 
        'insti': lambda x: list(set(x)),
        }).reset_index()
    auteurs2.to_csv('auteurs2.csv')

    auteurs3 = df.groupby(['insti']).agg({
    'doi': lambda x: list(set(x)),
    }).reset_index()
    auteurs3.to_csv('auteurs3.csv')

    auteurs4 = df.groupby(['pays']).agg({
    'insti': lambda x: list(set(x)),
    }).reset_index()
    auteurs4.to_csv('auteurs4.csv')

    prenom_AUTEUR = auteurs2['prenom'].tolist()
    nom_AUTEUR = auteurs2['nom'].tolist()
    email_AUTEUR = auteurs2['email'].tolist()

    laboratoire_LABO = auteurs3['insti'].tolist()
    pays_PAYS = auteurs4['pays'].tolist()
    
    doi_index = {doi: i for i, doi in enumerate(listedoi)}
    labo_index = {labo: i for i, labo in enumerate(laboratoire_LABO)}
    
    auteur_id_AUT_ART, article_id_AUT_ART = [], []
    labo_id_LAB_AUT, auteur_id_LAB_AUT = [], []

    for auteur in range(len(auteurs2)):

        for doi in auteurs2['doi'][auteur]:
            auteur_id_AUT_ART.append(auteur+1)
            article_id_AUT_ART.append(doi_index[doi]+1)

        for labo in auteurs2['insti'][auteur]:
            if type(labo)!=float:
                auteur_id_LAB_AUT.append(auteur+1)
                labo_id_LAB_AUT.append(labo_index[labo]+1)
    
    labo_id_LAB_ART, article_id_LAB_ART = [], []

    for labo in range(len(auteurs3)):
        
        for doi in auteurs3['doi'][labo]:
            labo_id_LAB_ART.append(labo+1)
            article_id_LAB_ART.append(doi_index[doi]+1)

    labo_id_LAB_PAYS, pays_id_LAB_PAYS = [], []

    for pays in range(len(auteurs4)):
        
        for labo in auteurs4['insti'][pays]:
            pays_id_LAB_PAYS.append(pays+1)
            labo_id_LAB_PAYS.append(labo_index[labo]+1)
    
    return prenom_AUTEUR, nom_AUTEUR, email_AUTEUR, auteur_id_AUT_ART, article_id_AUT_ART, labo_id_LAB_AUT, auteur_id_LAB_AUT, laboratoire_LABO, labo_id_LAB_ART, article_id_LAB_ART, pays_PAYS, labo_id_LAB_PAYS, pays_id_LAB_PAYS