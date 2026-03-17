from skills.process_document import process_document
from monitoring.logger import logger

def document_agent(path):
    logger.info(f"DocumentAgent processing file: {path}")
    return process_document(path)
