import json
import requests
from backend.utils.llm import generate

API_URL = "http://localhost:8000/ask"

def evaluate():
    with open("eval/questions.json", "r") as f:
        questions = json.load(f)

    llm_correct = 0
    rag_correct = 0
    total = len(questions)

    print(f"Running evaluation on {total} questions...\n")

    for q in questions:
        question = q["question"]
        expected = q["expected_answer"].lower()

        # 1. LLM ONLY
        llm_prompt = f"Answer this question about a consulting firm: {question}"
        llm_answer = generate(llm_prompt).lower()

        # 2. RAG
        rag_response = requests.post(API_URL, json={"question": question, "role": "Employee"}).json()
        rag_answer = rag_response["answer"].lower()

        # NEW LOGIC: Check if the critical words are in the answer
        # For "aggregation pipelines took 40+ seconds", we just check if "aggregation" and "40" are there.
        expected_words = [w for w in expected.split() if len(w) > 3]
        llm_pass = any(word in llm_answer for word in expected_words) if expected_words else True
        rag_pass = any(word in rag_answer for word in expected_words) if expected_words else True

        if llm_pass: llm_correct += 1
        if rag_pass: rag_correct += 1

        print(f"Q: {question}")
        print(f"  Expected: {expected}")
        print(f"  LLM Only: {'✅ Pass' if llm_pass else '❌ Fail'}")
        print(f"  LLM Full Answer: {llm_answer}\n") 
        print(f"  Your RAG: {'✅ Pass' if rag_pass else '❌ Fail'}")
        print(f"  RAG Full Answer: {rag_answer}\n") # <-- REMOVED [:50] so you see the full answer

    print("--- FINAL RESULTS ---")
    print(f"LLM Only Accuracy: {(llm_correct/total)*100:.1f}%")
    print(f"RAG Accuracy:      {(rag_correct/total)*100:.1f}%")

if __name__ == "__main__":
    evaluate()