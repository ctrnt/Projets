import numpy as np

def filedotjson(auteurs,bigali,doi):
    for auteur in auteurs:

        prenom = np.nan
        nom = np.nan
        email = np.nan
        labo = np.nan
        insti = np.nan
        pays = np.nan

        keys=auteur.keys()

        if 'first' in keys:
            prenom = auteur['first']

        if 'last' in keys:
            nom = auteur['last']

        if 'email' in keys:
            email = auteur['email']

        if 'affiliation' in keys:
            keys2=auteur['affiliation'].keys()
            if 'laboratory' in keys2:
                labo = auteur['affiliation']['laboratory']

            if 'institution' in keys2:
                insti = auteur['affiliation']['institution']

            if 'location' in keys2:
                keys3=auteur['affiliation']['location'].keys()
                if 'country' in keys3:
                    pays = auteur['affiliation']['location']['country']

        insti=choixlabo(labo,insti)

        bigali.append([doi,prenom,nom,email,insti,pays])
    return bigali

def choixlabo(labo,insti):
    if len(str(insti))>=len(str(labo)):
        return insti
    else:
        return labo