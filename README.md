## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

#### Déploiement

Le déploiement du site se fait via un Pipeline CircleCI : https://app.circleci.com/pipelines/github/Pierre12412
Les changements sur GitHub sont détéctés et le pipeline s'active en effectuant les actions suivantes dans cet ordre :

- Le Build de l'application avec les tests, l'activation d'un environnement python et l'installation de requirements.txt
- Si le build réussit : La nouvelle image de l'application est publiée à Docker Hub : https://hub.docker.com/repository/docker/pierre124/dockerhub
- Si la publication est réussie : heroku déploie l'application via git : https://oc-lettings-8.herokuapp.com/

#### Configurations Requises :
- Les requirements avec un environnement virtuel Python 3.9
- Git fonctionnel vers le repo de l'application
- Le fichier .circleci avec à l'intérieur la config.yml du pipeline
- Les fichiers .dockerignore et Dockerfile pour la création de la nouvelle image
- Le fichier Procfile pour le déploiement sur Heroku
- GitHub connecté à CircleCI
- L'application Heroku créée en amont

- Les variables suivante dans les variables d'environnement de l'application CircleCI :
	- DOCKERHUB_PASSWORD 
	- DOCKERHUB_USERNAME --> Connexion à DockerHub
	- HEROKU_API_KEY
	- HEROKU_APP_NAME --> Connexion à Heroku

- Les variables suivantes dans les variables d'environnement de l'application Heroku :
	-DSN (clé pour Sentry)
	-SECRET_KEY (clé secrète Django)

#### Etapes nécessaires:

1 - Créer tout les fichiers nécessaires avec :
	-Dans .circleci le fichier config.yml ci-dessous, remplacer <nom-app-dockerhub> par le nom de votre application DockerHub
	-Dans Procfile (sans extension, espaces importants, sans guillemets): 
		"web: gunicorn wsgi:application"
	-Dans Dockerfile les lignes de code ci-dessous
	-Dans .dockerignore : */venv

2- Créer un compte Sentry, créer un projet django, dans les paramètres récupérer le Security Token (pour la suite --> variable environnement virtuel DSN Heroku)

3- Créer l'application Heroku avec les variables d'environnement nécessaires et associer GitHub

4- Connecter CircleCI à Github

5- Dans les Projects CircleCI lancer Set Up Project et sélectionner la branche du repo du projet avec le config.yml

6- Dans CircleCI, entrer les variables d'environnement nécessaires (assurez vous d'avoir l'accès au DockerHub et à Heroku)

7- Push le projet dans Git

8- Vérifier que le Pipeline s'est bien executé

9- Aller sur le site de l'application : https://<nameapp>.herokuapp.com/




-------------------------- Config.yml ---------------------------------
```
version: 2.1
jobs:
  build:
    docker:
      - image: circleci/python:3.9
    steps:
      - checkout
      - restore_cache:
          key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
      - run:
          name: Activate Env/Install Requirements
          command: |
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
      - save_cache:
          key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
          paths:
            - "venv"
      - run:
          name: Running tests
          command: |
            . venv/bin/activate
            pytest
      - store_artifacts:
          path: test-reports/
          destination: python_app
  container:
    docker:
      - image: circleci/python:3.9
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.6
      - run:
          name: Publish Docker Image to Docker Hub
          command: |
            echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin
            docker build --tag dockerhub .
            docker tag dockerhub <nom-app-dockerhub>
            docker push <nom-app-dockerhub>

orbs:
  heroku: circleci/heroku@0.0.10
workflows:
  build_app:
    jobs:
      - build
      - container:
          requires:
            - build
          filters:
            branches:
              only:
                - main
      - heroku/deploy-via-git:
          requires:
            - container
          filters:
            branches:
              only:
                - main

```
-------------------------- Dockerfile ---------------------------------
```
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
EXPOSE 8000
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```
