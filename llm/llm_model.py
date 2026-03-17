from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model = "mistral",
    temperature=0.2
    # ,base_url="http://ollama:11434"
)