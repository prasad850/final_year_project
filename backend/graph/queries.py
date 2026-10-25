"""Reusable Cypher queries."""
from backend.graph.neo4j_client import run_query


def find_expert_by_keyword(keyword: str) -> dict | None:
    """Return the person who knows the skill matching keyword."""
    rows = run_query(
        """MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
           WHERE toLower(s.name) CONTAINS toLower($kw)
           RETURN p.name AS name, s.name AS skill LIMIT 1""",
        kw=keyword,
    )
    return rows[0] if rows else None


def find_expert_by_problem(problem_keyword: str) -> dict | None:
    """Return who solved a problem matching the keyword."""
    rows = run_query(
        """MATCH (p:Person)-[:SOLVED]->(s:Solution)
           MATCH (prob:Problem)-[:SOLVED_BY]->(s)
           WHERE toLower(prob.text) CONTAINS toLower($kw)
           RETURN p.name AS name, prob.text AS problem LIMIT 1""",
        kw=problem_keyword,
    )
    return rows[0] if rows else None