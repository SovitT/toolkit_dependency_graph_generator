import json
from collections import Counter

with open("dependency_graph.json", "r", encoding="utf-8") as f:
    graph = json.load(f)

edges = graph["edges"]

print("TOTAL NODES:", len(graph["nodes"]))
print("TOTAL EDGES:", len(edges))

print("\nTOP 25 DEPENDENCY LABELS:")
for label, count in Counter(
    edge["label"] for edge in edges
).most_common(25):
    print(f"{label:25} {count}")

print("\nSAMPLE DEPENDENCIES:")
for edge in edges[:30]:
    print(
        edge["from"],
        " --> ",
        edge["to"],
        " | ",
        edge["label"]
    )

print("\nCHECKING EXPECTED RELATIONSHIPS:")

expected = [
    ("GITHUB_LIST_REPOSITORY_ISSUES",
     "GITHUB_CREATE_AN_ISSUE_COMMENT", "issue_number"),

    ("GITHUB_LIST_PULL_REQUESTS",
     "GITHUB_MERGE_A_PULL_REQUEST", "pull_number")
]

for source, target, label in expected:
    found = any(
        e["from"] == source
        and e["to"] == target
        and e["label"] == label
        for e in edges
    )

    print(f"{source} -> {target}: {found}")