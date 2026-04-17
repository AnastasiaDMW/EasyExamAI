from prometheus_client import Counter, Histogram

# сколько запросов
request_counter = Counter(
    "easyexam_requests_total",
    "Total number of requests"
)

# какой агент используется чаще
agent_calls = Counter(
    "easyexam_agent_calls",
    "Agent usage",
    ["agent"]
)

token_usage = Histogram(
    "easyexam_token_usage",
    "Token usage",
    ["type"],
    buckets=[10, 50, 100, 200, 500, 1000, 2000, 4000]
)

# latency системы
request_latency = Histogram(
    "easyexam_request_latency_seconds",
    "Request latency"
)

# latency retrieval
retrieval_latency = Histogram(
    "easyexam_retrieval_latency_seconds",
    "Retrieval latency"
)

# latency LLM
llm_latency = Histogram(
    "easyexam_llm_latency_seconds",
    "LLM generation latency"
)

# количество retrieved документов
retrieved_docs = Histogram(
    "easyexam_retrieved_docs",
    "Number of retrieved documents"
)