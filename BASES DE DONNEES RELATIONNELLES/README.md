/!\ INSTRUCTIONS POUR LANCER LE PROJET SUR VOTRE PC /!\

- Télécharger l'archive au lien suivant : https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge?resource=download
- Extraire l'archive
- Supprimer dans l'archive le répertoire 'cord_embeddings'
- Télécharger le fichier 'Projet.zip' et l'extraire
- Glisser l'archive dans le dossier 'PEUPLEMENT' du projet

/!\ CREATION BASE DE DONNEES /!\
- Ouvrir pgAdmin4
- Clic droit 'Servers' -> 'Register' -> 'Server...'
- Dans l'onglet 'General', renseigner un nom dans le champ 'Name' (choix sans incidence sur la suite)
- Dans l'onglet 'Connection':
	- Rentrer 'localhost' dans le champ 'Hostname/address'
	- Rentrer 'dbpasswd' dans le champ 'Password'

- Cliquer sur le serveur créé, puis clic droit 'Databases' -> 'Create' -> 'Database...'
- Dans l'onglet 'General', ecrire 'DBCOVID' dans le champ 'Database'

- Dans l'invite de commandes:
	- Rentrer 'cd chemin_vers_dossier/PROJET/DJANGO/projetapp/'
	- Rentrer 'python manage.py makemigrations' puis 'python manage.py migrate'
	- Rentrer 'cd chemin_vers_dossier/PROJET/PEUPLEMENT/'
	- Executer le fichier 'main.py' avec la commande: 'python main.py'

/!\ LANCEMENT DU SERVEUR /!\
- Dans l'invite de commandes:
	- Rentrer 'cd chemin_vers_dossier/PROJET/DJANGO/projetapp/'
	- Rentrer 'python manage.py runserver'

- Vous pouvez desormais acceder au site en vous rendant sur l'url : 'localhost:8000'
