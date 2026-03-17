import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evals.eval_runner import (
    eval_routing,
    eval_retrieval,
    eval_latency,
    eval_end_to_end
)

def test_routing():
    accuracy = eval_routing()
    assert accuracy >= 0.5

def test_retrieval():
    score = eval_retrieval()
    assert score >= 0.5

def test_latency():
    avg_latency = eval_latency()
    assert avg_latency < 15

def test_end_to_end():
    eval_end_to_end()