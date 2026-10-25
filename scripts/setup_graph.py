"""Create Neo4j constraints. Run once."""
from backend.graph.schema import setup_schema

if __name__ == "__main__":
    setup_schema()