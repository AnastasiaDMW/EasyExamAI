import time
import tiktoken

from llm.llm_model import llm
from utils.load_prompt import load_prompt
from monitoring.metrics import llm_latency, token_usage
from monitoring.logger import logger

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str):
    return len(enc.encode(text))

tutor_prompt = load_prompt("prompts/tutor_prompt.txt")

def explain_topic(question, context=None):
    logger.info(f"Generating explanation for question: {question}")
    
    prompt = tutor_prompt.format(
        question=question,
        context=context or ""
    )

    input_tokens = count_tokens(prompt)

    start = time.time()
    response = llm.invoke(prompt)
    latency = time.time() - start

    output_tokens = count_tokens(response)

    logger.info(f"Input tokens: {input_tokens}")
    logger.info(f"Output tokens: {output_tokens}")

    llm_latency.observe(latency)
    token_usage.labels(type="input").observe(input_tokens)
    token_usage.labels(type="output").observe(output_tokens)

    logger.info(f"LLM response generated in {latency:.3f}s")
    return {
        "answer": response,
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "total": input_tokens + output_tokens
        }
    }