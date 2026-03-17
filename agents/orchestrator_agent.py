from llm.llm_model import llm
from skills.semantic_search import semantic_search
from utils.load_prompt import load_prompt
from agents.tutor_agent import tutor_agent
from agents.test_agent import test_agent
from agents.document_agent import document_agent
from monitoring.logger import logger

router_prompt = load_prompt("prompts/orchestrator_prompt.txt")

def orchestrator(user_input=None, task=None, payload=None):

    logger.info(f"Orchestrator received request: user_input={user_input}, task={task}")

    if task == "DOCUMENT" and payload:
        response = document_agent(payload)
        return {
            "task": "DOCUMENT",
            "agent": "DocumentAgent",
            "response": response
        }

    prompt = router_prompt.format(user_input=user_input)
    logger.info("Sending routing prompt to LLM")
    decision = llm.invoke(prompt).strip().upper()
    logger.info(f"Router decision: {decision}")
    if decision == "TEST":
        logger.info("Routing to TestAgent")
        response = test_agent(user_input)
        return {
            "task": "TEST",
            "agent": "TestAgent",
            "response": response
        }
    else:
        logger.info("Routing to TutorAgent")
        context = semantic_search(user_input)
        response = tutor_agent(user_input, context=context)
        return {
            "task": "TUTOR",
            "agent": "TutorAgent",
            "response": response
        }