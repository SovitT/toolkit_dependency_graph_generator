import json

with open("github_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def resolve_ref(ref, root):
    """Resolve local JSON schema references."""
    if not ref.startswith("#/"):
        return None

    current = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict):
            return None
        current = current.get(part)

    return current


def extract_fields(schema, root, path="", visited=None):
    """Extract nested output fields, following refs and arrays."""
    if visited is None:
        visited = set()

    if not isinstance(schema, dict):
        return []

    fields = []

    ref = schema.get("$ref")
    if ref:
        if ref in visited:
            return []
        target = resolve_ref(ref, root)
        if target:
            fields.extend(
                extract_fields(target, root, path, visited | {ref})
            )

    for name, child in schema.get("properties", {}).items():
        child_path = f"{path}.{name}" if path else name

        if isinstance(child, dict) and (
            "properties" in child or "$ref" in child or "items" in child
        ):
            fields.extend(
                extract_fields(child, root, child_path, visited.copy())
            )
        else:
            fields.append(child_path)

    if "items" in schema:
        fields.extend(
            extract_fields(
                schema["items"], root, path + "[]", visited.copy()
            )
        )

    for key in ("anyOf", "oneOf", "allOf"):
        for option in schema.get(key, []):
            fields.extend(
                extract_fields(option, root, path, visited.copy())
            )

    return fields


targets = [
    "GITHUB_LIST_REPOSITORY_ISSUES",
    "GITHUB_CREATE_AN_ISSUE_COMMENT",
    "GITHUB_LIST_PULL_REQUESTS",
    "GITHUB_MERGE_A_PULL_REQUEST"
]

for tool in catalog:
    if tool.get("slug") not in targets:
        continue

    output = tool.get("outputParameters", {})

    print("\n" + "=" * 65)
    print("TOOL:", tool["slug"])
    print("TOP-LEVEL KEYS:", list(tool.keys()))

    inputs = tool.get("inputParameters", {})
    print("REQUIRED INPUTS:", inputs.get("required", []))

    fields = extract_fields(output, output)

    print("\nEXTRACTED OUTPUT FIELDS:")
    for field in sorted(set(fields)):
        print("  -", field)

    print("TOTAL OUTPUT FIELDS:", len(set(fields)))

print("\nInspection complete!")