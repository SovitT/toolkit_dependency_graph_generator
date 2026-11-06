# Toolkit Dependency Graph Generator

A generalized dependency graph generator that analyzes toolkit catalogs, identifies relationships between tool inputs and outputs, and generates an interactive visualization of tool dependencies.

## Overview

Modern AI agents use multiple tools to complete complex tasks. However, understanding which tools depend on other tools can be challenging, especially when working with large tool catalogs.

This project addresses that challenge by automatically analyzing tool schemas and identifying potential dependencies between tools.

For example, one tool may return an `issue_number`, while another tool requires the same `issue_number` as an input. The generator identifies this relationship and creates a directed edge between the two tools.

The solution is designed to work with different toolkit catalogs rather than relying on hardcoded tool relationships.

## Key Features

- **Dynamic Catalog Parsing:** Reads toolkit information directly from a JSON catalog.
- **Input and Output Analysis:** Extracts tool input and output parameters.
- **Dependency Detection:** Identifies potential relationships by matching compatible input and output fields.
- **Graph Generation:** Represents tools as nodes and dependencies as directed edges.
- **Interactive Visualization:** Generates an HTML interface to search tools and explore their relationships.
- **Graph Validation:** Includes automated self-checks to validate the generated graph structure.
- **Reusable Architecture:** Avoids hardcoding individual tool relationships.

## Project Architecture

```text
toolkit-dependency-graph-generator/
│
├── src/
│   ├── generate.ts
│   └── selfcheck.ts
│
├── github_catalog.json
├── dependency_graph.json
├── visualize.py
├── dependency_graph.html
├── generator.json
├── package.json
└── README.md
```

## How It Works

The generator follows these steps:

1. **Load Catalog:** Reads the toolkit catalog provided through the command line.
2. **Parse Tool Schemas:** Extracts tool identifiers, input parameters, and output parameters.
3. **Identify Dependencies:** Compares output fields from one tool with input fields from other tools.
4. **Build Graph:** Creates nodes for tools and directed edges for identified dependencies.
5. **Export JSON:** Saves the generated graph as `dependency_graph.json`.
6. **Visualize Results:** Uses a Python script to generate an interactive HTML visualization.
7. **Validate Output:** Runs automated checks to verify the generated graph.

## Example

Consider two GitHub tools:

**Producer Tool:**

`GITHUB_LIST_REPOSITORY_ISSUES`

Produces an issue number.

**Consumer Tool:**

`GITHUB_CREATE_AN_ISSUE_COMMENT`

Requires an issue number.

The generator represents this relationship as:

```json
{
  "nodes": [
    {
      "id": "GITHUB_LIST_REPOSITORY_ISSUES",
      "service": "issues"
    },
    {
      "id": "GITHUB_CREATE_AN_ISSUE_COMMENT",
      "service": "issues"
    }
  ],
  "edges": [
    {
      "from": "GITHUB_LIST_REPOSITORY_ISSUES",
      "to": "GITHUB_CREATE_AN_ISSUE_COMMENT",
      "label": "issue_number"
    }
  ]
}
```

### Understanding the Graph

- **Nodes:** Individual tools in the toolkit.
- **Edges:** Dependencies between tools.
- **From:** The tool that produces the required information.
- **To:** The tool that consumes the information.
- **Label:** The parameter connecting the two tools.

## Technology Stack

| Technology | Purpose |
|---|---|
| TypeScript | Dependency graph generation |
| Node.js | Runtime environment |
| Python | Visualization generation |
| HTML, CSS, JavaScript | Interactive visualization |
| JSON | Toolkit catalog and graph storage |
| npm | Dependency and script management |

## Installation and Setup

### Prerequisites

- Node.js
- npm
- Python 3.x
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/toolkit-dependency-graph-generator.git
```

```bash
cd toolkit-dependency-graph-generator
```

### 2. Install Dependencies

```bash
npm install --legacy-peer-deps
```

### 3. Generate the Dependency Graph

Provide the toolkit catalog path:

```bash
npm run generate -- github_catalog.json
```

The generator creates:

```text
dependency_graph.json
```

### 4. Generate the Visualization

```bash
python visualize.py
```

Open the generated HTML file in your browser:

```bash
start dependency_graph.html
```

### 5. Run Validation

```bash
npm run selfcheck
```

This checks the generated graph structure, node and edge counts, provenance, and labeled dependencies.

## Sample Results

The current GitHub catalog execution produced:

| Metric | Result |
|---|---:|
| Tools processed | 893 |
| Generated nodes | 893 |
| Generated edges | 10,519 |
| Provenance ratio | 100% |
| Self-check | Passed |

*Note: These are results from the current GitHub catalog run. A 100% provenance ratio confirms that graph edges reference catalog tools; it does not guarantee that every inferred dependency is semantically correct.*

## Visualization Features

The generated HTML visualization provides:

- Search functionality for finding tools.
- Configurable node display limits.
- Visual representation of tool connections.
- Incoming dependency information.
- Outgoing dependency information.
- Dependency field labels.

## Limitations and Future Improvements

Some tools may contain parameters with similar names but different meanings. Matching fields by name can therefore produce false-positive dependencies.

Potential future improvements include:

- Advanced semantic matching of input and output parameters.
- More accurate nested JSON schema analysis.
- Better handling of ambiguous parameter names.
- Dependency confidence scoring.
- Improved graph layout and filtering.
- Support for additional toolkit catalog formats.

## Use Cases

- AI agent tool orchestration.
- API dependency discovery.
- Automated workflow planning.
- Tool relationship analysis.
- Understanding large tool ecosystems.

## Author

**Sovit Thakre**

MCA – Data Science

Interested in Data Science, Python Development, AI, and building practical automation solutions.

## License

This project is available for educational and development purposes. Add a license file if you intend to distribute it under a specific open-source license.
