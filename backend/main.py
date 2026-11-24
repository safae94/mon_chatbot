# 0. Réglages pour Mac - TOUT EN HAUT
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

# 1. Importer les outils
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 2. Charger la clé Gemini depuis .env
load_dotenv()

# 3. Rouvrir l'armoire FAISS (avec le MÊME modèle que index.py)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
)
db = FAISS.load_local("../faiss_index", embeddings, allow_dangerous_deserialization=True)

# 4. Le LLM qui écrit les réponses
llm_main = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.7, max_retries=1, timeout=60)
llm_backup = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7, max_retries=1, timeout=60)
llm = llm_main.with_fallbacks([llm_backup])

# 5. Le chercheur : renvoie les 3 fiches les plus proches
retriever = db.as_retriever(search_kwargs={"k": 3})

# 6. Les consignes pour le LLM
SYSTEM_PROMPT = """
You are a helpful assistant.
Use the context to answer the question in max three sentences.
If you don't know, just say don't know.
Context: {context}
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
])

# 7. Assembler la chaîne : chercher -> remplir les consignes -> Gemini
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# 8. Ouvrir le guichet
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

# 9. Le format de la question reçue : {"text": "..."}
class Query(BaseModel):
    text: str

# 10. Les adresses du guichet
@app.get("/")
def home():
    return {"message": "RAG API is running!"}

@app.post("/query")
def query_rag(query: Query):
    response = rag_chain.invoke({"input": query.text})
    return {"answer": response.get("answer", "No answer found")}