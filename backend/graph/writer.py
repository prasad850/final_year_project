"""Write extracted facts to Neo4j with full provenance."""
import hashlib
from backend.graph.neo4j_client import run_query


def _stable_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]
    return f"{prefix}_{h}"


def write_document(source: str, meta: dict = None) -> None:
    """Create the Document node. Call ONCE per file, before write_extraction."""
    meta = meta or {}
    run_query(
        """
        MERGE (d:Document {id: $source})
        SET d.path = $source,
            d.title = $title,
            d.doc_type = $doc_type,
            d.team = $team,
            d.tenant_id = 'nova'
        """,
        source=source,
        title=meta.get("title", source.split("/")[-1]),
        doc_type=meta.get("type", "markdown"),
        team=meta.get("team", ""),
    )


def _link_evidence(node_label: str, node_id: str, source: str) -> None:
    """Create the EVIDENCED_IN edge from a fact back to its source doc."""
    run_query(
        f"""
        MATCH (d:Document {{id: $source}})
        MATCH (n:{node_label} {{id: $node_id}})
        MERGE (n)-[:EVIDENCED_IN]->(d)
        """,
        source=source, node_id=node_id,
    )


def _link_mentions(label: str, name: str, source: str) -> None:
    """Create MENTIONS edge from Document to entity."""
    run_query(
        f"""
        MATCH (d:Document {{id: $source}})
        MATCH (n:{label} {{name: $name}})
        MERGE (d)-[:MENTIONS]->(n)
        """,
        source=source, name=name,
    )


def write_extraction(source: str, facts: dict) -> None:
    """Persist everything from extract_facts() with full provenance."""

    # --- Entities ---
    for p in facts.get("people", []):
        run_query("MERGE (n:Person {name: $name})", name=p["name"])
        _link_mentions("Person", p["name"], source)

    for c in facts.get("clients", []):
        run_query(
            "MERGE (n:Client {name: $name}) SET n.industry = $ind",
            name=c["name"], ind=c.get("industry", ""),
        )
        _link_mentions("Client", c["name"], source)

    for pr in facts.get("projects", []):
        run_query(
            "MERGE (n:Project {name: $name}) SET n.type = $t",
            name=pr["name"], t=pr.get("type", ""),
        )
        _link_mentions("Project", pr["name"], source)

    for s in facts.get("skills", []):
        run_query("MERGE (n:Skill {name: $name})", name=s)
        _link_mentions("Skill", s, source)

    # --- Decisions ---
    for d in facts.get("decisions", []):
        did = _stable_id("dec", source, d["text"])
        run_query(
            """MERGE (n:Decision {id: $id})
               SET n.text = $text, n.reason = $reason, n.status = $status""",
            id=did, text=d["text"], reason=d.get("reason", ""),
            status=d.get("status", "accepted"),
        )
        _link_evidence("Decision", did, source)

        if d.get("decided_by"):
            run_query(
                """MATCH (dec:Decision {id: $id})
                   MERGE (p:Person {name: $name})
                   MERGE (p)-[:DECIDED]->(dec)""",
                id=did, name=d["decided_by"],
            )

    # --- Problems ---
    for pb in facts.get("problems", []):
        pid = _stable_id("prob", source, pb["text"])
        run_query(
            "MERGE (n:Problem {id: $id}) SET n.text = $text, n.severity = $sev",
            id=pid, text=pb["text"], sev=pb.get("severity", "medium"),
        )
        _link_evidence("Problem", pid, source)

    # --- Solutions ---
    for sol in facts.get("solutions", []):
        sid = _stable_id("sol", source, sol["text"])
        run_query("MERGE (n:Solution {id: $id}) SET n.text = $text",
                  id=sid, text=sol["text"])
        _link_evidence("Solution", sid, source)

        if sol.get("applied_by"):
            run_query(
                """MATCH (s:Solution {id: $id})
                   MERGE (p:Person {name: $name})
                   MERGE (p)-[:SOLVED]->(s)""",
                id=sid, name=sol["applied_by"],
            )

    # --- Explicit relationships from LLM ---
    for r in facts.get("relationships", []):
        rel = r["type"]
        if rel not in {"WORKED_ON", "HAD_PROBLEM", "SOLVED", "DECIDED", "FOR_CLIENT"}:
            continue
        run_query(
            f"""MATCH (a) WHERE a.name = $from OR a.id = $from
                MATCH (b) WHERE b.name = $to OR b.id = $to
                MERGE (a)-[:{rel}]->(b)""",
            **{"from": r["from"], "to": r["to"]},
        )