import time
import tiktoken

from llm.llm_model import llm
from skills.semantic_search import semantic_search
from utils.load_prompt import load_prompt
from monitoring.metrics import llm_latency, token_usage
from monitoring.logger import logger

test_prompt = load_prompt("prompts/test_prompt.txt")

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str):
    return len(enc.encode(text))

def generate_test(topic):
    logger.info(f"Generating test for topic: {topic}")

    context = semantic_search(topic)
    prompt = test_prompt.format(
        context=context,
        topic=topic
    )

    input_tokens = count_tokens(prompt)

    start = time.time()
    result = llm.invoke(prompt)
    latency = time.time() - start

    output_tokens = count_tokens(result)

    llm_latency.observe(latency)

    token_usage.labels(type="input").observe(input_tokens)
    token_usage.labels(type="output").observe(output_tokens)

    logger.info(f"Input tokens: {input_tokens}")
    logger.info(f"Output tokens: {output_tokens}")

    logger.info(f"Test generation finished in {latency:.3f}s") 
    return {
            "answer": result,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "total": input_tokens + output_tokens
            }
        }