"""Neo4j driver — one connection, reused."""
from neo4j import GraphDatabase
from backend.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def run_query(cypher: str, **params) -> list[dict]:
    with get_driver().session() as session:
        return [record.data() for record in session.run(cypher, **params)]