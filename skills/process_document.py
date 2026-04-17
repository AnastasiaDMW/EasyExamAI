import os
import time
import tiktoken

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from memory.rag_pipeline import vector_db
from llm.llm_model import llm
from monitoring.metrics import llm_latency, token_usage
from utils.load_prompt import load_prompt
from monitoring.logger import logger

document_prompt = load_prompt("prompts/document_prompt.txt")

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str):
    return len(enc.encode(text))

def load_document(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext == ".md" or ext == ".txt":
        loader = TextLoader(path)
    elif ext == ".docx":
        loader = Docx2txtLoader(path)
    else:
        raise ValueError("Unsupported file format")
    return loader.load()


def process_document(path):
    logger.info(f"Processing document: {path}")

    docs = load_document(path)
    logger.info(f"Loaded {len(docs)} document sections")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)
    logger.info(f"Document split into {len(chunks)} chunks")

    for chunk in chunks:
        chunk.metadata["source"] = path

    vector_db.add_documents(chunks)
    logger.info("Document chunks added to vector database")

    full_text = "\n".join([doc.page_content for doc in docs])

    prompt = document_prompt.format(document=full_text)
    input_tokens = count_tokens(prompt)

    start = time.time()
    summary = llm.invoke(prompt)
    latency = time.time() - start

    output_tokens = count_tokens(summary)

    llm_latency.observe(latency)

    token_usage.labels(type="input").observe(input_tokens)
    token_usage.labels(type="output").observe(output_tokens)

    logger.info(f"Input tokens: {input_tokens}")
    logger.info(f"Output tokens: {output_tokens}")
    logger.info("Document summary generated")
    
    return {
        "status": "indexed",
        "summary": summary
    }