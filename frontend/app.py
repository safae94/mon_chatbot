# 1. Importer les outils
import streamlit as st      # crée la page web
import requests             # envoie la question au guichet

# 2. L'adresse du guichet (main.py)
API_URL = "http://127.0.0.1:8000/query"

# 3. Le titre de la page
st.title("Document Chatbot")
st.write("Pose des questions sur les documents du dossier knowledge_base")

# 4. La mémoire du chat (Streamlit relance tout le script à chaque action)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Réafficher les anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. La zone où j'écris ma question
if prompt := st.chat_input("Ask me anything ..."):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)

    # 7. Demander la réponse au guichet et l'afficher
    with st.chat_message("ai"):
        with st.spinner("Thinking ..."):
            try:
                res = requests.post(API_URL, json={"text": prompt})
                res.raise_for_status()
                answer = res.json()["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "ai", "content": answer})
            except Exception as e:
                st.error(f"api error {e}")