import os
from dotenv import load_dotenv
from groq import Groq
from backend.app.services.vector_store import build_index, search_index

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def prepare_document(pdf_id: str, text: str):
    chunks = []
    chunk_size = 600
    overlap = 100
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap

    build_index(pdf_id, chunks)


def answer_question(pdf_id: str, question: str) -> str:
    results = search_index(pdf_id, question)

    if not results:
        return "No relevant information found."

    # Combine top chunks as context
    context = "\n\n".join(results)

    # Build prompt
    prompt = f"""You are a helpful assistant answering questions about a document.
Use ONLY the context provided below to answer the question.
If the answer is not in the context, say "I couldn't find that information in the document."
Keep your answer clear, concise and direct.

Context:
{context}

Question: {question}

Answer:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback to raw chunk if Groq fails
        return f"(AI answer unavailable: {str(e)})\n\n{results[0]}"