ROUTING_TESTS = [
    {
        "question": "Generate 3 exam questions about neural networks",
        "expected_agent": "TestAgent"
    },
    {
        "question": "Explain what a multi-agent system is",
        "expected_agent": "TutorAgent"
    },
]

RETRIEVAL_TESTS = [
    {
        "query": "neural networks",
        "expected_keyword": "neural networks"
    },
    {
        "query": "backpropagation",
        "expected_keyword": "backpropagation"
    },
    {
        "query": "gradient descent",
        "expected_keyword": "gradient descent"
    }
]

E2E_TESTS = [
    "What is EasyExamAI?",
    "Explain the architecture of the system",
    "Generate test questions about AI"
]