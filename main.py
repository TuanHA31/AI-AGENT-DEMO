import os
from llm.hf_client import HFChat
from rag.ingest import create_or_load_vector_store
from rag.retriever import retrieve_context
from dotenv import load_dotenv
from memory import ConversationMemory

load_dotenv()

with open("document.txt", "r", encoding="utf-8") as f:
    text = f.read()

db = create_or_load_vector_store(text)

llm = HFChat(
    api_key=os.getenv("HF_TOKEN"),
    model="meta-llama/Meta-Llama-3-8B-Instruct"
)
memory = ConversationMemory(max_turns=5)

while True:
    question = input("\nYou: ")
    if question.lower() in ["exit", "quit"]:
        break

    context = retrieve_context(db, question)

    memory.add_user_message(question)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Answer based only on the given context."
        }
    ]

    messages.extend(memory.get_messages())

    messages.append({
        "role": "user",
        "content": f"""
Context:
{context}

Question:
{question}
"""
    })
    answer = llm.chat(messages)

    print("\nAI:", answer)

    memory.add_ai_message(answer)