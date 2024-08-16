# Utiliser une image Python officielle comme base
FROM python:3.12-slim

# Installer Git pour pouvoir cloner le dépôt
RUN apt-get update && apt-get install -y git && apt-get clean

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Cloner le dépôt GitHub dans le répertoire de travail
RUN git clone https://github.com/BerthetQuentin/BotDiscord .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Indiquer quelle commande exécuter pour démarrer l'application
CMD ["python", "main.py"]
