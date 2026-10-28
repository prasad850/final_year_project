from backend.graph.neo4j_client import run_query
from backend.utils.llm import generate
import json

def find_expert(question: str) -> dict:
    # 1. Ultra-strict prompt
    prompt = f"""Extract 1 to 3 TECHNICAL keywords (like AWS, ERP, GDPR, Kubernetes) from this question. 
    If the question is not about technology or business, return an empty array: {{"keywords": []}}
    Return ONLY a JSON object. Example: {{"keywords": ["AWS", "ERP"]}}
    
    Question: {question}"""
    
    try:
        raw = generate(prompt, json_mode=True, temperature=0.0)
        data = json.loads(raw)
        keywords = data.get("keywords", [])
    except Exception as e:
        print(f"LLM keyword extraction failed: {e}.")
        keywords = []

    # 2. NUCLEAR FILTER: Ban "us", "u.s", "president", and anything short
    banned_words = {"us", "u.s", "u.s.", "president", "who", "is", "the", "and", "for", "what", "why", "was", "we"}
    keywords = [k for k in keywords if len(k) >= 4 and k.lower() not in banned_words]

    print(f"🔍 DEBUG: Filtered keywords: {keywords}")

    if not keywords:
        return None 

    # 3. Strict Cypher Query: ONLY look at Skills and Projects, NOT Decisions or raw text
    cypher = """
        MATCH (p:Person)-[r:HAS_SKILL|WORKED_ON]->(n:Skill|Project)
        WHERE any(keyword IN $keywords WHERE 
            toLower(n.name) CONTAINS toLower(keyword)
        )
        RETURN p.name AS expert_name, count(r) AS score, collect(DISTINCT n.name) AS matched_topics
        ORDER BY score DESC
        LIMIT 1
    """
    
    results = run_query(cypher, keywords=keywords)
    
    if results:
        best_match = results[0]
        topics_list = best_match["matched_topics"]
        topics = ", ".join(topics_list[:3]) if topics_list else "related topics"
        clean_name = best_match["expert_name"].replace(".", " ").title()
        
        return {
            "name": clean_name,
            "reason": f"has worked on {topics}"
        }
    
    return None