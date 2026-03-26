import os
from dotenv import load_dotenv
from groq import Groq

from rag.pipeline import build_vector_db
from utils.classifier import classify_query
from utils.memory import add_to_memory, get_memory

# Load env
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load DB (cached)
nec_db = build_vector_db("data/nec")
wattmonk_db = build_vector_db("data/wattmonk")


def retrieve_context(db, query):
    docs = db.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    sources = [
        f"{doc.metadata.get('source', 'unknown')} (page {doc.metadata.get('page', 'N/A')})"
        for doc in docs
    ]

    return context, sources


def suggest_questions(query):
    return [
        f"Tell me more about {query}",
        f"Give examples related to {query}",
        f"Why is {query} important?",
        f"Explain {query} in simple terms"
    ]


def get_confidence(context):
    if context.strip() == "":
        return "Medium"
    elif len(context) < 300:
        return "Medium"
    else:
        return "High"


def chat(query):
    intent = classify_query(query)

    context = ""
    sources = []

    # Use RAG only when needed
    if intent == "nec":
        context, sources = retrieve_context(nec_db, query)

    elif intent == "wattmonk":
        context, sources = retrieve_context(wattmonk_db, query)

    memory = "\n".join([f"Q: {q} A: {a}" for q, a in get_memory()])

    # ✅ FINAL PROMPT (LANGUAGE FIXED)
    prompt = f"""
You are a smart AI assistant like ChatGPT.

IMPORTANT:
- Always reply in the SAME language as the user's question
- English → English
- Hindi → Hindi
- Hinglish → Hinglish
- Be natural, not dramatic

Capabilities:
- Understand casual queries
- If context is available → use it
- If not → answer normally
- Never unnecessarily switch language

Conversation History:
{memory}

Context:
{context}

User Query:
{query}

Give a helpful, natural response:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Error: {str(e)}"

    add_to_memory(query, answer)

    suggestions = suggest_questions(query)
    confidence = get_confidence(context)

    return answer, ", ".join(set(sources)), intent, suggestions, confidence