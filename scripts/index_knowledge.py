import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from memory.rag_pipeline import vector_db
from monitoring.logger import logger

knowledge_folder = "knowledge"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

for file in os.listdir(knowledge_folder):
    path = f"{knowledge_folder}/{file}"
    loader = TextLoader(path)
    docs = loader.load()
    chunks = splitter.split_documents(docs)
    vector_db.add_documents(chunks)

logger.info("Knowledge base indexed")
logger.info("Кол-во документов в базе: %d", len(vector_db.get()["ids"]))