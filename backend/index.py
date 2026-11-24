# 0. Réglages pour Mac (évitent le plantage "abort") - TOUT EN HAUT
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

# 1. Importer les outils
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# 2. Les chemins (../ = remonter d'un dossier)
DATA_PATH = "../knowledge_base"
FAISS_PATH = "../faiss_index"

# 3. LIRE les .txt et les .pdf
txt_loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader,
                             loader_kwargs={"encoding": "utf-8"})
pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
docs = txt_loader.load() + pdf_loader.load()
print(f"Documents chargés : {len(docs)}")

# 4. DÉCOUPER en fiches de 1000 caractères (150 en commun entre voisines)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = splitter.split_documents(docs)
print(f"Nombre de morceaux : {len(docs)}")

# 5. DONNER UNE ADRESSE (vecteur) à chaque fiche - "cpu" pour le Mac
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
)

# 6. RANGER dans FAISS et sauvegarder
db = FAISS.from_documents(docs, embeddings)
db.save_local(FAISS_PATH)
print("FAISS index created successfully and saved locally!")