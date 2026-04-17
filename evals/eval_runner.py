import time

from agents.orchestrator_agent import orchestrator
from skills.semantic_search import retrieve_documents
from evals.eval_dataset import ROUTING_TESTS, RETRIEVAL_TESTS, E2E_TESTS


def eval_routing():
    correct = 0

    for test in ROUTING_TESTS:
        result = orchestrator(user_input=test["question"])
        predicted = result["agent"]

        if predicted == test["expected_agent"]:
            correct += 1

        print("Question:", test["question"])
        print("Expected:", test["expected_agent"])
        print("Predicted:", predicted)
        print()

    accuracy = correct / len(ROUTING_TESTS)

    print("Routing accuracy:", accuracy)

    return accuracy

def eval_retrieval():
    success = 0

    for test in RETRIEVAL_TESTS:
        docs = retrieve_documents(test["query"])

        if not docs:
            continue

        top_doc_text = docs[0].page_content.lower()

        if test["expected_keyword"].lower() in top_doc_text:
            success += 1

        print("Query:", test["query"])
        print("Top result:", top_doc_text[:150])
        print()

    score = success / len(RETRIEVAL_TESTS)
    print("Retrieval score:", score)
    return score

def eval_latency():
    times = []

    for q in E2E_TESTS:
        start = time.time()

        orchestrator(user_input=q)

        end = time.time()

        latency = end - start
        times.append(latency)

        print("Question:", q)
        print("Latency:", latency)
        print()

    avg_latency = sum(times) / len(times)

    print("Average latency:", avg_latency)

    return avg_latency


def eval_end_to_end():
    for q in E2E_TESTS:

        result = orchestrator(user_input=q)

        print("Question:", q)
        print("Agent:", result["agent"])
        print("Answer:", result["response"])
        print("-" * 40)