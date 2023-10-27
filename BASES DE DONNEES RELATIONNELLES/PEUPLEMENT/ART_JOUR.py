def choixurl(liste):
    for lien in liste:
        if 'doi' in lien:
            return lien
        if lien == liste[-1]:
            return lien
        
def articles_journaux(df):
    df = df.drop(['source_x','cord_uid','sha', 'license','abstract','authors','mag_id','who_covidence_id','arxiv_id','s2_id'], axis=1)

    df=df[df['doi'].isnull() | ~df[df['doi'].notnull()].duplicated(subset='doi',keep='first')]
    df=df[df['pdf_json_files'].isnull() | ~df[df['pdf_json_files'].notnull()].duplicated(subset='pdf_json_files',keep='first')]
    df=df[df['pmc_json_files'].isnull() | ~df[df['pmc_json_files'].notnull()].duplicated(subset='pmc_json_files',keep='first')]
    
    df = df.reset_index(drop=True)
    
    doi_ARTICLE = df['doi'].tolist()
   
    indice=1
    for i in range(0,len(doi_ARTICLE)):
        if type(doi_ARTICLE[i])==float:
            doi_ARTICLE[i] = 'no_doi_'+str(indice)
            indice+=1

    titre_ARTICLE = df['title'].tolist()
    date_ARTICLE = df['publish_time'].tolist()
    lien_ARTICLE = df['url'].tolist()

    for i in range(len(lien_ARTICLE)):
        if type(lien_ARTICLE[i])==str and len(lien_ARTICLE[i].split(';'))>1:
            lien_ARTICLE[i] = choixurl(lien_ARTICLE[i].split(';'))

    listepmcid = df['pmcid'].tolist()
    listepubmed = df['pubmed_id'].tolist()

    journaux = df['journal'].tolist()

    nom_journal_JOURNAL = []
    journal_id_ARTICLE = []
    jour_dict = {}

    for j in journaux:
        if j not in jour_dict:
            jour_dict[j] = len(nom_journal_JOURNAL)
            nom_journal_JOURNAL.append(j)
        journal_id_ARTICLE.append(jour_dict[j]+1)

    doi_ART_FULL, titre_ART_FULL, date_ART_FULL = [], [], []
    doi_ART_YEAR, titre_ART_YEAR, date_ART_YEAR = [], [], []
    for i in range(len(date_ARTICLE)):
        if len(str(date_ARTICLE[i]))==10:
            doi_ART_FULL.append(doi_ARTICLE[i])
            titre_ART_FULL.append(titre_ARTICLE[i])
            date_ART_FULL.append(date_ARTICLE[i])
        if len(str(date_ARTICLE[i]))==4:
            doi_ART_YEAR.append(doi_ARTICLE[i])
            titre_ART_YEAR.append(titre_ARTICLE[i])
            date_ART_YEAR.append(date_ARTICLE[i])

    return df,listepmcid, listepubmed, doi_ARTICLE, titre_ARTICLE, date_ARTICLE, lien_ARTICLE, nom_journal_JOURNAL, journal_id_ARTICLE, doi_ART_FULL, titre_ART_FULL, date_ART_FULL, doi_ART_YEAR, titre_ART_YEAR, date_ART_YEAR