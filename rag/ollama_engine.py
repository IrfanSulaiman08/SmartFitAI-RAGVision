import os
from langchain_community.llms import Ollama

# =========================
# LOAD DOCUMENTS
# =========================
def load_docs():
    folder = "rag/documents"
    docs = {}

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        with open(path, "r", encoding="utf-8") as f:
            docs[file.replace(".txt", "")] = f.read()

    return docs


# =========================
# YOUR OLD LOGIC
# =========================
def get_relevant_text(question):
    docs = load_docs()
    q = question.lower()

    if any(w in q for w in ["diet", "food", "eat", "nutrition"]):
        text = docs.get("diet", "")

    elif any(w in q for w in ["exercise", "fitness", "workout", "muscle", "squat"]):
        text = docs.get("fitness", "")

    elif any(w in q for w in ["recovery", "pain", "injury"]):
        text = docs.get("recovery", "")

    else:
        text = ""

    # FIND BEST LINE
    lines = text.split("\n")

    best_line = ""
    max_score = 0

    for line in lines:
        score = sum(1 for word in q.split() if word in line.lower())

        if score > max_score:
            max_score = score
            best_line = line

    return best_line


# =========================
# LOAD MODEL
# =========================
llm = Ollama(model="llama3")


# =========================
# FINAL FUNCTION
# =========================
def ask_rag(question):

    context = get_relevant_text(question)

    # =========================
    # IF CONTEXT FOUND
    # =========================
    if context != "":
        prompt = f"""
You are a fitness and health assistant.

Use the given context to answer clearly.

Context:
{context}

Question:
{question}

Answer in 2-3 lines:
"""

    # =========================
    # IF NO CONTEXT
    # =========================
    else:
        prompt = f"""
You are a fitness and health assistant.

Answer the question clearly.

Question:
{question}

Answer in 2-3 lines:
"""

    # =========================
    # CALL OLLAMA
    # =========================
    response = llm.invoke(prompt)

    return f"💡 Answer:\n\n{response}"
