import time

from llm.llm_model import llm
from skills.semantic_search import semantic_search
from utils.load_prompt import load_prompt
from monitoring.metrics import llm_latency
from monitoring.logger import logger

test_prompt = load_prompt("prompts/test_prompt.txt")

def generate_test(topic):
    logger.info(f"Generating test for topic: {topic}")

    context = semantic_search(topic)
    prompt = test_prompt.format(
        context=context,
        topic=topic
    )

    start = time.time()
    result = llm.invoke(prompt)
    latency = time.time() - start
    llm_latency.observe(latency)

    logger.info(f"Test generation finished in {latency:.3f}s")    
    return result