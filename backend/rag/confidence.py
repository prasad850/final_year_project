"""Decide if we have enough to answer."""
from backend.config import CONFIDENCE_DISTANCE_THRESHOLD

def assess(question : str, results:list[dict])-> dict:

    if not results:
        return{"confidence":0.0 , "enough":False, "reason":"No results found."}

    best_distance= min(r["distance"] for r in results)
    confidence = round(max(0.0, 1-best_distance), 2)

    if best_distance > CONFIDENCE_DISTANCE_THRESHOLD:
        return{
            "confidence":confidence, "enough":False, "reason":"low similarity."
        }

    return {"confidence": confidence, "escalate": False, "reason": "ok"}