import threading, time, asyncio, sys
from abc import ABC, abstractmethod

etat = {'ser': 1, 'prep': 1, 'cmd': 1}
lock = threading.Lock()

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

    def ajouter(self, postit):
        with lock:
            self.postits.append(postit)
            if self.verbose >= 1:
                print(f"[{self.__class__.__name__}] post-it '{postit}' embroché | {time.time()-self.launch_time}")
            if self.verbose >= 2:
                print(f"[{self.__class__.__name__}] état={self.postits} | {time.time()-self.launch_time}")

    def retirer(self):
        with lock:
            if self.postits:
                supp = self.postits.pop()
                if self.verbose >= 1:
                    print(f"[{self.__class__.__name__}] post-it '{supp}' libéré | {time.time()-self.launch_time}")
                if self.verbose >= 2:
                    print(f"[{self.__class__.__name__}] état={self.postits} | {time.time()-self.launch_time}")
                if not self.postits and self.verbose >= 1:
                    print(f"Pic est vide | {time.time()-self.launch_time}")
                return supp
            else:
                return None

class Bar(Accessoire):
    def __init__(self, verbose, launch_time):
        self.plateaux = []
        self.verbose = verbose
        self.launch_time = launch_time

    def ajouter(self, plateau):
        with lock:
            self.plateaux.append(plateau)
            if self.verbose >= 1:
                print(f"[{self.__class__.__name__}] '{plateau}' reçu | {time.time()-self.launch_time}")
            if self.verbose >= 2:
                print(f"[{self.__class__.__name__}] état={self.plateaux} | {time.time()-self.launch_time}")

    def retirer(self):
        with lock:
            if self.plateaux:
                supp = self.plateaux.pop()
                if self.verbose >= 1:
                    print(f"[{self.__class__.__name__}] '{supp}' évacué | {time.time()-self.launch_time}")
                if self.verbose >= 2:
                    print(f"[{self.__class__.__name__}] état={self.plateaux} | {time.time()-self.launch_time}")
                if not self.plateaux and self.verbose >= 1:
                    print(f"Bar est vide | {time.time()-self.launch_time}")
                return supp
            else:
                return None

class Serveur:
    def __init__(self, pic_commandes, pic_addition, bar, commandes, launch_time):
        self.pic = pic_commandes
        self.pic_addition = pic_addition
        self.bar = bar
        self.commandes = commandes
        self.launch_time = launch_time
        print(f"[{self.__class__.__name__}] prêt pour le service ! | {time.time()-self.launch_time}")

    async def prendre_commande(self):
        global etat
        while self.commandes and etat['cmd'] == 1:
            commande = self.commandes.pop()
            print(f"[{self.__class__.__name__}] je prends commande de '{commande}' | {time.time()-self.launch_time}")
            self.pic.ajouter(commande)
            await asyncio.sleep(0.5)

        print(f"[{self.__class__.__name__}] il n'y a plus de commande à prendre | {time.time()-self.launch_time}")
        etat['cmd'] = 0

    async def servir(self):
        global etat
        while etat['ser'] != 0 or etat['prep'] != 0:
            if len(self.bar.plateaux) >0:
                etat['ser'] = 1
                plateau = self.bar.retirer()
                self.pic_addition.ajouter(plateau)
                print(f"[{self.__class__.__name__}] je sers '{plateau}' | {time.time()-self.launch_time}")
                await asyncio.sleep(1.0)
            elif etat['prep'] == 1:
                etat['ser'] = 1
                await asyncio.sleep(0)
            else:
                etat['ser'] = 0
                await asyncio.sleep(0)

    async def serveur_fonctions(self):
        await self.prendre_commande()
        await self.servir()

class Barman:
    def __init__(self, pic_commandes, pic_addition, bar, launch_time):
        self.pic = pic_commandes
        self.pic_addition = pic_addition
        self.bar = bar
        self.launch_time = launch_time
        print(f"[{self.__class__.__name__}] prêt pour le service ! | {time.time()-self.launch_time}")

    async def preparer(self):
        global etat
        while etat['ser'] != 0 or etat['prep'] != 0:
            if len(self.pic.postits) > 0 or etat['cmd'] == 1:
                etat['prep'] = 1
                commande = self.pic.retirer()
                if commande is not None:
                    print(f"[{self.__class__.__name__}] je commence la fabrication de '{commande}' | {time.time()-self.launch_time}")
                    await asyncio.sleep(3.0)
                    print(f"[{self.__class__.__name__}] je termine la fabrication de '{commande}' | {time.time()-self.launch_time}")
                    self.bar.ajouter(commande)
            else:
                etat['prep'] = 0
                await asyncio.sleep(0)

    async def encaisser_addition(self):
        global etat
        while self.pic_addition.postits or etat['cmd']!=0 or etat['ser']!=0 or etat['prep']!=0:
            if self.pic_addition.postits:
                commande = self.pic_addition.retirer()
                print(f"[{self.__class__.__name__}] j'encaisse l'addition pour '{commande}' | {time.time()-self.launch_time}")
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(0)
        print(f"[{self.__class__.__name__}] Plus d'encaissements. | {time.time()-self.launch_time}")

    async def barman_fonctions(self):
        await self.preparer()
        await self.encaisser_addition()