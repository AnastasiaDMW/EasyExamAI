from skills.explain_topic import explain_topic
from monitoring.logger import logger

def tutor_agent(question: str, context: str = None):
    logger.info(f"TutorAgent explaining question: {question}")
    return explain_topic(question=question, context=context)