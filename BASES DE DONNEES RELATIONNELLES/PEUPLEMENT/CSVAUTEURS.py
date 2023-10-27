import os,json
import pandas as pd
from TRAITEMENT_JSON import filedotjson

def auteursetcie(df,listedoi):
    pathpdf=os.getcwd()+'//archive//document_parses//pdf_json//'
    pathpmc=os.getcwd()+'//archive//document_parses//pmc_json//'

    bigali=[]

    list_pdf = os.listdir(pathpdf)
    list_pmc = os.listdir(pathpmc)

    for i in range(len(df)):
        doi=listedoi[i]

        if type(df['pdf_json_files'][i])==str:
            for j in df['pdf_json_files'][i].split(';'):
                if str(j).split('/')[-1] in list_pdf:
                    with open(pathpdf+str(j).split('/')[-1]) as f: 
                        file=json.load(f)
                    auteurs=file['metadata']['authors']
                    bigali=filedotjson(auteurs,bigali,doi)

        if type(df['pmc_json_files'][i])==str:
            for j in df['pmc_json_files'][i].split(';'):
                if str(j).split('/')[-1] in list_pmc:
                    with open(pathpmc+str(j).split('/')[-1]) as f:
                        file=json.load(f)
                    auteurs=file['metadata']['authors']
                    bigali=filedotjson(auteurs,bigali,doi)

        if i%200000==0:
            print(i)

    auteurs_csv = pd.DataFrame(bigali, columns=['doi', 'prenom', 'nom', 'email', 'insti', 'pays'])
    
    auteurs_csv.to_csv('auteurs.csv')

    return auteurs_csv