import os, re
import numpy as np
import pandas as pd

def themes_ssthemes_types(listedoi, listepmc, listepubmed):
    path = os.getcwd() + '//archive//Kaggle//target_tables'
    data = []
    regexpmc = r"\bPMC\d{7}\b"
    regexpubmed = r"\b\d{8}\b"
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                
                theme = os.path.basename(root)
                sous_theme = os.path.splitext(file)[0]
                
                dfth = pd.read_csv(os.path.join(root, file))
                for i, row in dfth.iterrows():
                    
                    type = np.nan
                    if 'Study Type' in dfth.columns:
                        type = row['Study Type']
                        
                    if 'Study Link' in dfth.columns:
                        lien = row['Study Link']
                        
                        if 'PMC' in lien:
                            pmc = re.search(regexpmc, lien)
                            if pmc.group() in listepmc:
                                index=listepmc.index(pmc.group())
                                doi = listedoi[index]
                                data.append([doi, theme[2:], sous_theme, type])
        
                        elif '10.' in lien:
                            L = lien.split('10.')
                            doi = '10.' + '10.'.join(L[1:])
                            if doi in listedoi:
                                data.append([doi, theme[2:], sous_theme, type])
                        
                        elif 'pubmed' in lien:
                            pubmed = re.search(regexpubmed, lien)
                            if pubmed.group() in listepubmed:
                                index = listepubmed.index(pubmed.group())
                                doi = listedoi[index]
                                data.append([doi, theme[2:], sous_theme, type])

    dfthemes = pd.DataFrame(data, columns=['doi', 'theme', 'sous_theme', 'type'])

    nom_theme_THEME = dfthemes['theme'].unique().tolist()
    nom_sous_theme_SSTHEME = dfthemes['sous_theme'].unique().tolist()
    nom_type_TYPE = dfthemes['type'].unique().tolist()

    dfthemes2 = dfthemes.groupby('doi').agg({
    'sous_theme': lambda x: list(set(x)),
    'type': lambda x: list(set(x))
    }).reset_index()

    article_id_SSTHEMESARTICLE, sstheme_id_SSTHEMESARTICLE = [], []
    article_id_TYPESARTICLE, type_id_TYPESARTICLE = [], []

    for i in range(len(dfthemes2)):
        index_doi = listedoi.index(dfthemes2['doi'][i])
        for sstheme in dfthemes2['sous_theme'][i]:
            index_sstheme = nom_sous_theme_SSTHEME.index(sstheme)
            article_id_SSTHEMESARTICLE.append(index_doi+1)
            sstheme_id_SSTHEMESARTICLE.append(index_sstheme+1)

        for type in dfthemes2['type'][i]:
            if str(type)!='nan':
                index_type = nom_type_TYPE.index(type)
                article_id_TYPESARTICLE.append(index_doi+1)
                type_id_TYPESARTICLE.append(index_type+1)

    dfthemes3 = dfthemes.drop_duplicates(subset=['theme','sous_theme'],ignore_index=True)

    listethemes = dfthemes3['theme'].tolist()
    
    theme_id_SSTHEME = [nom_theme_THEME.index(theme) for theme in listethemes] 

    theme_id_SSTHEME = [x + 1 for x in theme_id_SSTHEME]

    dfthemes.to_csv('theme1.csv')
    dfthemes2.to_csv('theme2.csv')
    dfthemes3.to_csv('theme3.csv')
    
    return nom_theme_THEME, nom_sous_theme_SSTHEME, sstheme_id_SSTHEMESARTICLE, article_id_SSTHEMESARTICLE, theme_id_SSTHEME, nom_type_TYPE, type_id_TYPESARTICLE, article_id_TYPESARTICLE