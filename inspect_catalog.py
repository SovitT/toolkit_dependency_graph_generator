import json

with open("github_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print("Total tools:", len(catalog))

keywords = [
    "LIST_REPOSITORY_ISSUES",
    "CREATE_AN_ISSUE_COMMENT",
    "LIST_PULL_REQUESTS",
    "MERGE_A_PULL_REQUEST"
]

for tool in catalog:
    slug = tool.get("slug", "")

    if any(keyword in slug for keyword in keywords):
        print("\n" + "=" * 70)
        print("TOOL:", slug)
        print("NAME:", tool.get("name"))
        print("DESCRIPTION:", tool.get("description"))

        inputs = tool.get("inputParameters", {})
        outputs = tool.get("outputParameters", {})

        print("\nINPUT PARAMETERS:")
        print(json.dumps(inputs.get("properties", {}), indent=2))

        print("\nREQUIRED INPUTS:")
        print(inputs.get("required", []))

        print("\nOUTPUT PARAMETERS:")
        print(json.dumps(outputs.get("properties", {}), indent=2))

        print("\nOUTPUT DEFINITIONS:")
        print(json.dumps(outputs.get("$defs", {}), indent=2)[:2500])

print("\nInspection completed!")