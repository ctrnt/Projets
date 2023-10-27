import time, asyncio
from abc import ABC, abstractmethod

etat={'ser':1,'prep':1,'cmd':1}

class Accessoire(ABC):
    @abstractmethod
    def ajouter(self):
        pass

    @abstractmethod
    def retirer(self):
        pass

class Pic(Accessoire):
    def __init__(self, verbose, launch_time):
        self.postits = []
        self.verbose = verbose
        self.launch_time = launch_time

    def ajouter(self,postit):
        self.postits.append(postit)
        if self.verbose >= 1:
            print(f"[{self.__class__.__name__}] post-it '{postit}' embroché | {time.time()-self.launch_time}")
        if self.verbose >=2:
            print(f"[{self.__class__.__name__}] état={self.postits} | {time.time()-self.launch_time}")

    def retirer(self):
        supp = self.postits.pop()
        if self.verbose >= 1:
            print(f"[{self.__class__.__name__}] post-it '{supp}' libéré | {time.time()-self.launch_time}")
        if self.verbose >=2:
            print(f"[{self.__class__.__name__}] état={self.postits} | {time.time()-self.launch_time}")
        if self.postits == [] and self.verbose>=1:
            print(f"Pic est vide | {time.time()-self.launch_time}")
        return supp

class Bar(Accessoire):
    def __init__(self, verbose, launch_time):
        self.plateaux = []
        self.verbose = verbose
        self.launch_time = launch_time

    def ajouter(self,plateau):
        self.plateaux.append(plateau)
        if self.verbose >= 1:
            print(f"[{self.__class__.__name__}] '{plateau}' reçu | {time.time()-self.launch_time}")
        if self.verbose >=2:
            print(f"[{self.__class__.__name__}] état={self.plateaux} | {time.time()-self.launch_time}")

    def retirer(self):
        supp = self.plateaux.pop()
        if self.verbose >= 1:
            print(f"[{self.__class__.__name__}] '{supp}' évacué | {time.time()-self.launch_time}")
        if self.verbose >=2:
            print(f"[{self.__class__.__name__}] état={self.plateaux} | {time.time()-self.launch_time}")
        if self.plateaux == [] and self.verbose>=1:
            print(f"Bar est vide | {time.time()-self.launch_time}")
        return supp

class Serveur:
    def __init__(self,pic,bar,commandes, launch_time):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes
        self.launch_time = launch_time
        print(f"[{self.__class__.__name__}] prêt pour le service ! | {time.time()-self.launch_time}")

    async def prendre_commande(self):
        global etat
        while self.commandes!=[] and etat['cmd']==1:
            commande = self.commandes.pop()
            print(f"[{self.__class__.__name__}] je prends commande de '{commande}' | {time.time()-self.launch_time}")
            self.pic.ajouter(commande)
            await asyncio.sleep(0.5)
        
        print(f"[{self.__class__.__name__}] il n'y a plus de commande à prendre | {time.time()-self.launch_time}")
        etat['cmd']=0

    async def servir(self):
        global etat
        while  etat['ser']!=0 or etat['prep']!=0:
            if len(self.bar.plateaux)>0:
                etat['ser']=1
                plateau = self.bar.retirer()
                print(f"[{self.__class__.__name__}] je sers '{plateau}' | {time.time()-self.launch_time}")
                await asyncio.sleep(1.0)
            elif etat['prep']==1:
                etat['ser']=1
                await asyncio.sleep(0)
            else:
                etat['ser']=0
                await asyncio.sleep(0)

class Barman:
    def __init__(self, pic, bar, launch_time):
        self.pic = pic
        self.bar = bar
        self.launch_time = launch_time
        print(f"[{self.__class__.__name__}] prêt pour le service ! | {time.time()-self.launch_time}")

    async def preparer(self):
        global etat
        while etat['ser']!=0 or etat['prep']!=0:
            if len(self.pic.postits)>0 or etat['cmd']==1:
                etat['prep']=1
                commande = self.pic.retirer()
                print(f"[{self.__class__.__name__}] je commence la fabrication de '{commande}' | {time.time()-self.launch_time}")
                await asyncio.sleep(3.0)
                print(f"[{self.__class__.__name__}] je termine la fabrication de '{commande}' | {time.time()-self.launch_time}") 
                self.bar.ajouter(commande)
            else:
                etat['prep']=0
                await asyncio.sleep(0)