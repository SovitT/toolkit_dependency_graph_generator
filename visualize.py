import json
from pathlib import Path
from html import escape

with open("dependency_graph.json", encoding="utf-8") as f:
    graph = json.load(f)

nodes = graph["nodes"]
edges = graph["edges"]

data = json.dumps(graph).replace("</", "<\\/")

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tool Dependency Graph</title>
<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #101827;
  color: #e5e7eb;
}
header {
  padding: 20px;
  background: #1e293b;
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  align-items: center;
}
h2 { margin: 0; }
input, select, button {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #475569;
  background: #0f172a;
  color: white;
}
#stats { color: #94a3b8; }
#canvas {
  width: 100%;
  height: calc(100vh - 110px);
  overflow: hidden;
}
svg { width: 100%; height: 100%; }
line { stroke: #64748b; stroke-opacity: .4; }
circle { fill: #38bdf8; stroke: #e0f2fe; stroke-width: 1; }
circle:hover { fill: #f59e0b; }
text { fill: white; font-size: 11px; pointer-events: none; }
#details {
  position: fixed;
  right: 15px;
  bottom: 15px;
  padding: 14px;
  max-width: 330px;
  background: #1e293b;
  border: 1px solid #475569;
  border-radius: 8px;
  display: none;
  overflow-wrap: anywhere;
}
</style>
</head>
<body>
<header>
  <h2>Tool Dependency Graph</h2>
  <input id="search" placeholder="Search tool name...">
  <select id="limit">
    <option value="50">50 nodes</option>
    <option value="100" selected>100 nodes</option>
    <option value="200">200 nodes</option>
    <option value="500">500 nodes</option>
  </select>
  <button id="render">Render graph</button>
  <span id="stats"></span>
</header>
<div id="canvas">
<svg id="graph" viewBox="0 0 1200 750">
<g id="edges"></g>
<g id="nodes"></g>
</svg>
</div>
<div id="details"></div>
<script>
const graph = __GRAPH__;
const svg = document.getElementById("graph");
const edgeLayer = document.getElementById("edges");
const nodeLayer = document.getElementById("nodes");
const details = document.getElementById("details");

function draw() {
  const query = document.getElementById("search").value.toLowerCase();
  const limit = Number(document.getElementById("limit").value);

  let selected = graph.nodes.filter(n =>
    n.id.toLowerCase().includes(query)
  ).slice(0, limit);

  const ids = new Set(selected.map(n => n.id));

  let selectedEdges = graph.edges.filter(e =>
    ids.has(e.from) && ids.has(e.to)
  );

  const width = 1200, height = 750;
  const nodes = selected.map((n, i) => ({
    ...n,
    x: 600 + 270 * Math.cos(2 * Math.PI * i / Math.max(1, selected.length)),
    y: 375 + 270 * Math.sin(2 * Math.PI * i / Math.max(1, selected.length))
  }));

  const positions = new Map(nodes.map(n => [n.id, n]));

  edgeLayer.innerHTML = "";
  nodeLayer.innerHTML = "";

  selectedEdges.slice(0, 2500).forEach(e => {
    const a = positions.get(e.from);
    const b = positions.get(e.to);
    if (!a || !b) return;

    const line = document.createElementNS(
      "http://www.w3.org/2000/svg", "line"
    );
    line.setAttribute("x1", a.x);
    line.setAttribute("y1", a.y);
    line.setAttribute("x2", b.x);
    line.setAttribute("y2", b.y);
    line.setAttribute("stroke-width", "1");
    edgeLayer.appendChild(line);
  });

  nodes.forEach(n => {
    const group = document.createElementNS(
      "http://www.w3.org/2000/svg", "g"
    );

    const circle = document.createElementNS(
      "http://www.w3.org/2000/svg", "circle"
    );
    circle.setAttribute("cx", n.x);
    circle.setAttribute("cy", n.y);
    circle.setAttribute("r", "7");

    const label = document.createElementNS(
      "http://www.w3.org/2000/svg", "text"
    );
    label.setAttribute("x", n.x + 10);
    label.setAttribute("y", n.y + 4);
    label.textContent = n.id;

    group.appendChild(circle);
    group.appendChild(label);

    group.addEventListener("click", () => {
      const incoming = graph.edges.filter(e => e.to === n.id);
      const outgoing = graph.edges.filter(e => e.from === n.id);
      details.style.display = "block";
      details.innerHTML =
        "<b>" + n.id + "</b><hr>" +
        "Incoming dependencies: " + incoming.length +
        "<br>Outgoing dependencies: " + outgoing.length +
        "<br><br>" +
        incoming.slice(0, 12).map(e =>
          "← " + e.from + " (" + e.label + ")"
        ).join("<br>") +
        "<br><br>" +
        outgoing.slice(0, 12).map(e =>
          "→ " + e.to + " (" + e.label + ")"
        ).join("<br>");
    });

    nodeLayer.appendChild(group);
  });

  document.getElementById("stats").textContent =
    nodes.length + " visible nodes | " +
    selectedEdges.length + " visible edges";
}

document.getElementById("render").addEventListener("click", draw);
document.getElementById("search").addEventListener("input", draw);
document.getElementById("limit").addEventListener("change", draw);
draw();
</script>
</body>
</html>
""".replace("__GRAPH__", data)

Path("dependency_graph.html").write_text(html, encoding="utf-8")

print("Visualization created!")
print("Nodes:", len(nodes))
print("Edges:", len(edges))
print("File: dependency_graph.html")