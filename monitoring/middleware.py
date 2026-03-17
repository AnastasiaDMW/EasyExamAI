import time
from fastapi import Request
from monitoring.metrics import request_latency, request_counter

async def metrics_middleware(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    latency = time.time() - start

    request_counter.inc()
    request_latency.observe(latency)

    return response