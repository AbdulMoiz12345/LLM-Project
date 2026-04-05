import streamlit as st
from rag_pipeline import RAGPipeline

# -------------------------------
# Initialize RAG System
# -------------------------------
@st.cache_resource
def load_rag():
    return RAGPipeline(
        faiss_index_path="data/bank_knowledge.index",
        metadata_path="data/bank_metadata.pkl"
    )

rag = load_rag()

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Banking Assistant (RAG)",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Assistant (RAG System)")
st.markdown("Ask questions about banking policies, accounts, and services.")

# -------------------------------
# Session State for Chat History
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Display Chat History
# -------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# User Input
# -------------------------------
user_query = st.chat_input("Ask your question...")

if user_query:

    # Show user message
    st.chat_message("user").markdown(user_query)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    # -------------------------------
    # Get Response from RAG
    # -------------------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            response = rag.query(user_query)

            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })