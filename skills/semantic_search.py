import time

from memory.rag_pipeline import retriever
from monitoring.metrics import retrieval_latency, retrieved_docs
from monitoring.logger import logger

def retrieve_documents(query: str):
    logger.info(f"Retrieval started for query: {query}")

    start = time.time()
    docs = retriever.invoke(query)
    latency = time.time() - start

    retrieval_latency.observe(latency)
    retrieved_docs.observe(len(docs))

    logger.info(f"Retrieval finished. Docs found: {len(docs)} | latency: {latency:.3f}s")
    return docs

def semantic_search(query: str):
    docs = retrieve_documents(query)
    context = "\n".join([doc.page_content for doc in docs])
    logger.info(f"Semantic search built context with {len(docs)} chunks")
    return context