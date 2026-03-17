import time

from llm.llm_model import llm
from utils.load_prompt import load_prompt
from monitoring.metrics import llm_latency
from monitoring.logger import logger

tutor_prompt = load_prompt("prompts/tutor_prompt.txt")

def explain_topic(question, context=None):
    logger.info(f"Generating explanation for question: {question}")
    
    prompt = tutor_prompt.format(
        question=question,
        context=context or ""
    )

    start = time.time()
    response = llm.invoke(prompt)
    latency = time.time() - start
    llm_latency.observe(latency)

    logger.info(f"LLM response generated in {latency:.3f}s")
    return response