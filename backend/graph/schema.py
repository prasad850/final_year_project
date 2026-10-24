"""Create unique constraints so MERGE does not create duplicates."""
from backend.graph.neo4j_client import run_query


def setup_schema():
    """Run once after Neo4j starts."""
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Client) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (pr:Project) REQUIRE pr.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Decision) REQUIRE d.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Problem) REQUIRE p.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Solution) REQUIRE s.id IS UNIQUE",
    ]
    for c in constraints:
        run_query(c)
    print(f"Created {len(constraints)} constraints.")