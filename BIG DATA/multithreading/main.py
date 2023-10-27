import sys, time, asyncio, threading

from multithread import Pic, Bar, Serveur, Barman

def main():
    launch_time = time.time()
    try:
        verbose = int(sys.argv[1])
    except ValueError:
        print('la verbose doit être égale à 0, 1 ou 2')
        sys.exit()
    if verbose not in [0, 1, 2]:
        print('la verbose doit être égale à 0, 1 ou 2')
    else:
        commandes = sys.argv[2:]
        pic_commandes = Pic(verbose, launch_time)
        bar = Bar(verbose, launch_time)
        pic_addition = Pic(verbose, launch_time)

        barman1 = Barman(pic_commandes, pic_addition, bar, launch_time)
        serveur1 = Serveur(pic_commandes, pic_addition, bar, commandes, launch_time)

        thread_barman = threading.Thread(target=asyncio.run, args=(barman1.barman_fonctions(),))
        thread_serveur = threading.Thread(target=asyncio.run, args=(serveur1.serveur_fonctions(),))

        thread_barman.start()
        thread_serveur.start()

        thread_barman.join()
        thread_serveur.join()

if __name__ == "__main__":
    main()