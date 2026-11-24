# 🤖 Mon Chatbot RAG

Un chatbot qui répond aux questions **à partir de mes propres documents**, grâce à la technique **RAG** (Retrieval-Augmented Generation).

Au lieu de laisser l'IA répondre de mémoire (avec un risque d'erreurs ou d'inventions), le chatbot :
1. **cherche** les passages les plus pertinents dans une base de documents,
2. les **donne à l'IA** avec la question,
3. l'IA **rédige une réponse** basée uniquement sur ces passages.

Si l'information n'est pas dans les documents, le chatbot répond qu'il ne sait pas.

---

## 🧠 Fonctionnement

**Préparation (une seule fois)**
```
Site web ──► scrape.py ──► knowledge_base/ ──► index.py ──► faiss_index/
            (récupère       (texte brut)       (découpe en    (base de
             le texte)                          morceaux +     recherche)
                                                embeddings)
```

**À chaque question**
```
Utilisateur ──► Streamlit ──► FastAPI ──► FAISS (3 passages les plus proches)
                                              │
Réponse ◄──── Streamlit ◄──── Gemini ◄────────┘
                           (rédige la réponse)
```

---

## 🛠️ Technologies

| Rôle | Outil |
|---|---|
| Récupération des données | Requests, BeautifulSoup |
| Embeddings (texte → vecteurs) | HuggingFace `all-MiniLM-L6-v2` |
| Base vectorielle | FAISS |
| Orchestration RAG | LangChain |
| Modèle de langage | Google Gemini (`gemini-3.5-flash`, avec modèle de secours) |
| API backend | FastAPI + Uvicorn |
| Interface | Streamlit |

---

## 📁 Structure du projet

```
mon-chatbot/
├── scraper/
│   └── scrape.py          # Récupère le texte d'une page web
├── knowledge_base/
│   └── webscraping.txt    # Documents utilisés par le chatbot
├── backend/
│   ├── index.py           # Découpe les documents et crée l'index FAISS
│   ├── main.py            # API FastAPI : recherche + appel à Gemini
│   └── requirements.txt   # Dépendances Python
└── frontend/
    └── app.py             # Interface de chat Streamlit
```

---

## 🚀 Installation et lancement

**1. Cloner le projet et créer l'environnement**
```bash
git clone https://github.com/safae94/mon_chatbot.git
cd mon_chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

**2. Ajouter sa clé API Gemini**

Créer un fichier `backend/.env` contenant :
```
GOOGLE_API_KEY=votre_cle_api
```
(clé gratuite sur [Google AI Studio](https://aistudio.google.com/))

**3. Construire l'index (une seule fois)**
```bash
cd backend
python3 index.py
```

**4. Lancer le backend** (terminal 1, depuis `backend/`)
```bash
python3 -m uvicorn main:app --reload
```
Documentation de l'API : http://127.0.0.1:8000/docs

**5. Lancer l'interface** (terminal 2, depuis la racine du projet)
```bash
source venv/bin/activate
streamlit run frontend/app.py
```
Puis ouvrir http://localhost:8501

---

## 💬 Exemples de questions

- *What is web scraping used for?*
- *What is contact scraping?*
- *What is the capital of Japan?* → le chatbot doit répondre qu'il ne sait pas (hors de ses documents)

---

## 🔧 Robustesse

- **Modèle de secours** : si le modèle Gemini principal est surchargé (erreurs 503 / 504), LangChain bascule automatiquement sur un second modèle (`with_fallbacks`).
- **Timeouts et limite de tentatives** : évite les requêtes bloquées indéfiniment.
- **Clé API protégée** : le fichier `.env` est exclu du dépôt grâce au `.gitignore`.

---



---

## 👩‍💻 Auteure

**Safae** — Master Informatique (Traitement de l'information et exploitation des données), formation Data Analyst.
