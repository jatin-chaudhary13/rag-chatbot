import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embeddings


def load_documents(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            docs.extend(loader.load())
    return docs


@st.cache_resource
def build_vector_db(folder_path):
    db_path = f"{folder_path}_faiss"

    if os.path.exists(db_path):
        return FAISS.load_local(db_path, get_embeddings(), allow_dangerous_deserialization=True)

    documents = load_documents(folder_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    db = FAISS.from_documents(docs, get_embeddings())
    db.save_local(db_path)

    return db