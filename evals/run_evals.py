import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evals.eval_runner import (
    eval_routing,
    eval_retrieval,
    eval_latency,
    eval_end_to_end
)

def run_all_evals():

    print("Test Routing Evaluation")
    eval_routing()

    print("\nTest Retrieval Evaluation")
    eval_retrieval()

    print("\nTest Latency Evaluation")
    eval_latency()

    print("\nTest End-to-End Examples")
    eval_end_to_end()


if __name__ == "__main__":
    run_all_evals()