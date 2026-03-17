from skills.generate_test import generate_test
from monitoring.logger import logger

def test_agent(topic):
    logger.info(f"TestAgent generating test for topic: {topic}")
    return generate_test(topic)