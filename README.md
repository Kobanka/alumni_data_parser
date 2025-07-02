# 📊 Extracteur d'Expériences Alumni

Une application web Streamlit pour extraire et structurer les données d'expériences professionnelles à partir de fichiers Excel d'alumni.

## 🚀 Fonctionnalités

- **Upload de fichiers Excel** : Interface simple pour uploader des fichiers .xlsx
- **Traitement automatique** : Extraction et structuration des expériences professionnelles
- **Téléchargement des résultats** : Génération d'un fichier Excel structuré
- **Interface intuitive** : Design moderne et facile à utiliser
- **Statistiques en temps réel** : Aperçu des données traitées

## 📋 Format des données d'entrée

Le fichier Excel doit contenir :
- **2 lignes d'en-tête** à ignorer
- **Colonnes requises** :
  - `NOM` : Nom de famille
  - `PRÉNOM(S)` : Prénom(s)
  - `EXPÉRIENCES` : Données d'expérience au format texte

### Format des expériences dans la colonne EXPÉRIENCES :
```
Poste - Entreprise
DD/MM/YYYY - DD/MM/YYYY
Localisation

Autre Poste - Autre Entreprise
DD/MM/YYYY - DD/MM/YYYY
Autre Localisation
```

## 🔧 Installation locale

1. Clonez ou téléchargez ce projet

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez l'application :
```bash
streamlit run app.py
```

4. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

## 🌐 Déploiement gratuit

### Option 1: Streamlit Cloud (Recommandé)

1. **Créez un compte GitHub** (si vous n'en avez pas)
2. **Uploadez votre code** :
   - Créez un nouveau repository sur GitHub
   - Uploadez les fichiers : `app.py`, `requirements.txt`, et `README.md`

3. **Déployez sur Streamlit Cloud** :
   - Allez sur [share.streamlit.io](https://share.streamlit.io)
   - Connectez-vous avec votre compte GitHub
   - Cliquez sur "New app"
   - Sélectionnez votre repository
   - Définissez le fichier principal : `app.py`
   - Cliquez sur "Deploy"

4. **Votre app sera disponible** à une URL publique gratuite !

### Option 2: Hugging Face Spaces

1. **Créez un compte** sur [huggingface.co](https://huggingface.co)
2. **Créez un nouveau Space** :
   - Allez dans "Spaces"
   - Cliquez sur "Create new Space"
   - Choisissez "Streamlit" comme SDK
   - Uploadez vos fichiers

### Option 3: Railway

1. **Créez un compte** sur [railway.app](https://railway.app)
2. **Connectez votre repository GitHub**
3. **Déployez automatiquement**

## 📊 Données de sortie

Le fichier Excel généré contient les colonnes suivantes :
- `ID` : Identifiant unique de l'expérience
- `Nom` : Nom de famille
- `Prénom` : Prénom(s)
- `Rôle` : Poste occupé
- `Entreprise` : Nom de l'entreprise
- `Localisation` : Lieu de travail
- `Durée` : Durée calculée de l'expérience

## 🛠️ Technologies utilisées

- **Streamlit** : Framework web pour Python
- **Pandas** : Manipulation des données
- **OpenPyXL** : Lecture/écriture des fichiers Excel
- **Python** : Langage de programmation

## 📝 Notes importantes

- Les fichiers uploadés ne sont pas stockés sur le serveur
- Le traitement se fait entièrement en mémoire
- L'application est sécurisée et respecte la confidentialité des données
- Taille maximale recommandée : 200MB par fichier

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez le format de votre fichier Excel
2. Assurez-vous que les colonnes requises sont présentes
3. Consultez les messages d'erreur affichés dans l'interface

---
*Développé avec ❤️ en utilisant Streamlit*
