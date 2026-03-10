import os
from llm.hf_client import HFChat
from rag.ingest import create_or_load_vector_store
from dotenv import load_dotenv
from agent.graph import build_graph

load_dotenv()

# Load knowledge document
with open("document.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Create or load vector store
db = create_or_load_vector_store(text)

# Initialize LLM
llm = HFChat(
    api_key=os.getenv("HF_TOKEN"),
    model="meta-llama/Meta-Llama-3-8B-Instruct"
)

# Build LangGraph workflow
graph = build_graph(db, llm)

print("AI Agent Ready (type 'exit' to quit)\n")

# Conversation state (memory)
state = {
    "messages": [],
    "context": "",
    "answer": ""
}

while True:

    question = input("You: ")

    if question.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    # Add new question to state
    state["question"] = question

    # Run graph
    result = graph.invoke(state)

    # Update state for next turn
    state = result

    print("AI:", result["answer"])

    print("\nDEBUG MEMORY:")
    for m in state["messages"]:
        print(m)
    print("------\n")