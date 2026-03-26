from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
import os

def load_documents(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            docs.extend(loader.load())
    return docs


def create_vectorstore(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)