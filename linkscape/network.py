from importlib import resources
import json
from typing import List
import base64


class Node:
    def __init__(self,
                 node_id: str,
                 label: str = None,
                 tooltip: str = None,
                 color: str = None,
                 level: int = None,
                 radius: int = 18,
                 stroke_color: str = None,
                 stroke_width: int = 2):
        self.node_id = node_id
        self.label = label
        self.tooltip = tooltip or label
        self.color = color or "#57C7E3"
        self.level = level
        self.radius = radius
        self.stroke_color = stroke_color or "#23B3D7"
        self.stroke_width = stroke_width

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False


class Edge:
    def __init__(self, source: str, target: str,
                 label: str = None,
                 color: str = "#94B3CC",
                 opacity: float = 1.0,
                 width: float = 1,
                 force: float = None):
        self.edge_id = 0
        self.label = label
        self.source = source
        self.target = target
        self.color = color
        self.opacity = opacity
        self.width = width
        self.force = force

    def __hash__(self):
        return hash(self.source + self.target)

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.source == other.source and self.target == other.target
        return False


class Network:

    def __init__(self, width: int = 800, height: int = 600,
                 x_levels: int = -1,
                 collision_radius: int = 8,
                 link_type: str = "link",
                 link_force: float = 0.3,
                 show_arrows: bool = True,
                 node_label_font_family: str = "Arial",
                 node_label_font_size: str = "12px",
                 node_label_color: str = "black",
                 link_label_font_family: str = "Arial",
                 link_label_font_size: str = "8px",
                 link_label_color: str = "#aaa",
                 background_color: str = "white"):
        self._html = resources.read_text("linkscape", "template.html")
        self._html = (self._html
                      .replace("$width", str(width))
                      .replace("$height", str(height))
                      .replace("$x_levels", str(x_levels))
                      .replace("$collision_radius", str(collision_radius))
                      .replace("$linkType", link_type)
                      .replace("$showArrows", "true" if show_arrows else "false")
                      .replace("$linkForce", str(link_force)))
        self._generate_styles(node_label_font_family, node_label_font_size, node_label_color,
                              link_label_font_family, link_label_font_size, link_label_color,
                              background_color)
        self._width = width
        self._height = height
        self.show_arrows = show_arrows

        self._nodes: set[Node] = set()
        self._edges: set[Edge] = set()

        self._edge_id_i = 0

    def _generate_styles(self,
                         node_label_font_family: str,
                         node_label_font_size: str,
                         node_label_color: str,
                         link_label_font_family: str,
                         link_label_font_size: str,
                         link_label_color: str,
                         background_color: str) -> None:
        self._html = self._html.replace("<head></head>", f"""<head>
    <style>
        .node-label {{
            font-family: "{node_label_font_family}";
                font-size: {node_label_font_size};
                fill: {node_label_color}
            }}

        .link-label {{
            font-family: "{link_label_font_family}";
            font-size: {link_label_font_size};
            fill: {link_label_color};
        }}

        svg {{
            background-color: {background_color};
        }}
    </style>
</head>""")

    def node(self, node_id: str, label: str | None = None) -> Node:
        """
        Create a new node and add it to the network.
        :param node_id: Node id.
        :param label: Node label.
        :return: The created node.
        """

        n = Node(node_id, label)
        if n in self._nodes:
            raise ValueError(f"Node with id '{node_id}' already exists.")

        self._nodes.add(n)
        return n

    def has_node(self, node_id: str) -> bool:
        """
        Check if a node with the given id exists in the network.
        :param node_id: Node id to check.
        :return: True if the node exists, False otherwise.
        """

        return any(n.node_id == node_id for n in self._nodes)

    def edge(self, source_id: str, target_id: str) -> Edge:
        edge = Edge(source_id, target_id)
        if edge in self._edges:
            raise ValueError(f"Edge between '{source_id}' and '{target_id}' already exists.")
        edge.edge_id = self._edge_id_i
        self._edge_id_i += 1
        self._edges.add(edge)
        return edge

    def has_edge(self, source_id: str, target_id: str) -> bool:
        return any(e.source == source_id and e.target == target_id for e in self._edges)

    def _render_data(self) -> str:
        r = self._html

        nodes = [{
            "id": n.node_id,
            "label": n.label,
            "tooltip": n.tooltip,
            "color": n.color,
            "level": n.level,
            "radius": n.radius,
            "stroke": n.stroke_color,
            "stroke_width": n.stroke_width
        } for n in self._nodes]

        links = [{
            "id": l.edge_id,
            "label": l.label,
            "source": l.source,
            "target": l.target,
            "color": l.color,
            "opacity": l.opacity,
            "width": l.width,
            "force": l.force
        } for l in self._edges]

        nodes_json = json.dumps(nodes)
        links_json = json.dumps(links)

        r = (r
             .replace("$data_nodes", nodes_json)
             .replace("$data_links", links_json))
        return r

    def _repr_html_(self):
        data = self._render_data()
        b64data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        url = f"data:text/html;charset=utf-8;base64,{b64data}"
        return f"<iframe src=\"{url}\" width=\"{self._width}\" height=\"{self._height}\" scrolling=\"no\" style=\"border:none !important;\"></iframe>"

    def save(self, path: str) -> None:
        with open(path, "w") as writer:
            writer.write(self._render_data())
