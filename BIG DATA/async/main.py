import sys, time, asyncio

from asynchronism import Pic, Bar, Serveur, Barman

async def main():
    launch_time = time.time()
    verbose = int(sys.argv[1])
    if verbose not in [0, 1, 2]:
        print('la verbose doit être égale à 0, 1 ou 2')
    else:
        commandes = sys.argv[2:]
        pic = Pic(verbose, launch_time)
        bar = Bar(verbose, launch_time)

        barman1 = Barman(pic, bar, launch_time)
        serveur1 = Serveur(pic, bar, commandes, launch_time)

        tasks = [
            serveur1.prendre_commande(),
            barman1.preparer(),
            serveur1.servir(),
        ]

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())