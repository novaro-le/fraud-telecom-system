#  Système de Détection de Fraude Télécom (CDR)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-Big%20Data-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-Machine%20Learning-green)
![FastAPI](https://img.shields.io/badge/FastAPI-API-success)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)

##  Description

Ce projet a été réalisé dans le cadre du Projet Tutoré de la Licence 3 Intelligence Artificielle et Big Data.

L'objectif est de détecter automatiquement les transactions frauduleuses à partir de données de type CDR (Call Detail Records) en utilisant des techniques de Big Data et de Machine Learning.

Le système combine :

- Apache Spark pour le traitement des données
- XGBoost pour la détection de fraude
- FastAPI pour l'API de prédiction
- Streamlit pour le dashboard interactif
- SQLite pour l'historique des prédictions
- Docker pour le déploiement

---

##  Objectifs

- Détecter les transactions frauduleuses
- Analyser les données télécoms à grande échelle
- Construire un modèle performant de Machine Learning
- Fournir des prédictions en temps réel
- Visualiser les résultats via un dashboard interactif

---

##  Technologies utilisées

| Domaine | Technologies |
|----------|-------------|
| Langage | Python |
| Big Data | Apache Spark, PySpark |
| Machine Learning | XGBoost, Scikit-Learn |
| Analyse de données | Pandas, NumPy |
| Visualisation | Plotly, Matplotlib |
| API | FastAPI |
| Dashboard | Streamlit |
| Base de données | SQLite |
| Conteneurisation | Docker, Docker Compose |
| Versioning | Git, GitHub |

---

##  Dataset

Le projet utilise le dataset **PaySim** disponible sur Kaggle.

Variables principales :

| Variable | Description |
|-----------|------------|
| step | Temps simulé |
| type | Type de transaction |
| amount | Montant |
| oldbalanceOrg | Ancien solde expéditeur |
| newbalanceOrig | Nouveau solde expéditeur |
| oldbalanceDest | Ancien solde destinataire |
| newbalanceDest | Nouveau solde destinataire |
| isFraud | Classe cible |
| isFlaggedFraud | Fraude signalée |

Types de transactions :

- CASH_IN
- CASH_OUT
- PAYMENT
- TRANSFER
- DEBIT

---

##  Architecture

```text
Dataset PaySim
       │
       ▼
Apache Spark
(Nettoyage + Prétraitement)
       │
       ▼
Feature Engineering
       │
       ▼
XGBoost
(Modèle ML)
       │
       ▼
FastAPI
(API de prédiction)
       │
 ┌─────┴─────┐
 ▼           ▼
SQLite   Streamlit
Historique Dashboard
```

---

## 📂 Structure du projet

```bash
fraud-telecom/
│
├── api/
│   ├── app.py
│   └── fraud_history.db
│
├── dashboard/
│   └── dashboard.py
│
├── model/
│   ├── fraud_model.pkl
│   └── label_encoders.pkl
│
├── data/
├── notebooks/
│
├── Dockerfile.api
├── Dockerfile.dashboard
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

##  Installation

### 1. Cloner le projet

```bash
git clone https://github.com/novaro-le/fraud-telecom-system.git
cd fraud-telecom-system
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Lancer l'API

```bash
uvicorn api.app:app --reload
```

Accès à Swagger :

```text
http://localhost:8000/docs
```

---

## 📈 Lancer le Dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

## 🐳 Déploiement Docker

Construire et lancer les services :

```bash
docker compose up --build
```

Arrêter :

```bash
docker compose down
```

---

## 🔌 API Endpoints

### POST /predict

Prédiction d'une transaction.

Exemple de réponse :

```json
{
  "prediction": "Fraud",
  "fraud_probability": 0.97
}
```

### GET /history

Retourne l'historique des prédictions.

### GET /stats

Retourne les statistiques enregistrées.

---

##  Fonctionnalités du Dashboard

✅ Prédiction de fraude

✅ Historique des transactions

✅ Statistiques globales

✅ Visualisations interactives

✅ Analyse des montants

✅ Répartition fraude / non fraude

---

## ⚠️ Remarque

Si le dashboard affiche :

> Aucune donnée disponible.

Cela ne constitue pas une erreur.

Aucune transaction n'a encore été enregistrée dans la base SQLite. Effectuez une simulation de transaction pour alimenter les statistiques et les graphiques.

---


---

## 🔗 GitHub

https://github.com/novaro-le/fraud-telecom-system