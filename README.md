
---

# Système de Détection de Fraude Télécom (CDR)

##  Description du projet

Ce projet vise à détecter les transactions frauduleuses dans un réseau télécom à partir de données **CDR (Call Detail Records)** en utilisant des techniques de **Big Data (Apache Spark)** et de **Machine Learning**.

Une application interactive (dashboard) est développée avec **Streamlit** pour visualiser les résultats, les analyses et les prédictions du modèle.

---

##  Objectifs

* Charger et traiter de grandes données avec **Apache Spark**
* Effectuer une analyse exploratoire des données (EDA)
* Nettoyer et transformer les données pour le Machine Learning
* Construire un modèle de détection de fraude
* Évaluer les performances du modèle (Accuracy, Precision, Recall, F1-score)
* Déployer un dashboard interactif avec **Streamlit**
* Fournir une interface simple pour tester des prédictions en temps réel

---

##  Approche du projet

1. **Collecte et chargement des données CDR**
2. **Traitement Big Data avec PySpark**
3. **Analyse exploratoire (EDA)**
4. **Feature engineering**
5. **Entraînement du modèle (Machine Learning)**
6. **Évaluation des performances**
7. **Déploiement avec Streamlit**

---

##  Technologies utilisées

*  Python
*  Apache Spark (PySpark)
*  Pandas, NumPy
*  Scikit-learn
*  Plotly, Matplotlib
*  Streamlit
*  Requests

---

## 📁 Structure du projet

```bash
fraud-detection-project/
│
├── data/                # Dataset CDR
├── notebooks/           # Jupyter notebooks (EDA, ML, tests)
├── models/              # Modèles entraînés (pickle / joblib)
├── app/                 # Application Streamlit
│   └── dashboard.py
├── api/                 # (optionnel) API FastAPI pour prédiction
├── database/            # SQLite (historique, logs)
├── docker/              # Configuration Docker (optionnel)
├── requirements.txt     # Dépendances Python
└── README.md
```

---

##  Installation et exécution

### 1.le projet

```bash
git clone https://github.com/ton-compte/fraud-detection-project.git
cd fraud-detection-project
```

### 2.Environnement virtuel

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ▶ Lancer l'application Streamlit

```bash
streamlit run app/dashboard.py
```

---

##  Résultats attendus

* Détection des transactions frauduleuses en temps réel
* Visualisation des tendances de fraude
* Analyse des comportements suspects
* Indicateurs de performance du modèle

---

##  Modèle Machine Learning

Le projet utilise un modèle supervisé de classification (ex: **Random Forest / XGBoost**) pour prédire si une transaction est :

*  Normale (0)
*  Frauduleuse (1)

---

##  Métriques d’évaluation

* Accuracy
* Precision
* Recall
* F1-score
* Matrice de confusion

---

---

##  Améliorations futures

* Intégration d’une API FastAPI pour les prédictions
* Déploiement Docker complet
* Ajout d’un système d’alertes en temps réel
* Amélioration du modèle avec Deep Learning

---
