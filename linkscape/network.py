from importlib import resources
import json
from typing import List
import base64


class Node:
    def __init__(self,
                 id: str,
                 label: str = None,
                 tooltip: str = None,
                 color: str = "#57C7E3", level: int = None,
                 radius: int = 18,
                 stroke_color: str = "#23B3D7",
                 stroke_width: int = 2):
        self.id = id
        self.label = label
        self.tooltip = tooltip or label
        self.color = color
        self.level = level
        self.radius = radius
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width


class Edge:
    def __init__(self, source: str, target: str,
                 label: str = None,
                 color: str = "#94B3CC",
                 opacity: float = 1.0,
                 width: float = 1,
                 force: float = None):
        self.id = 0
        self.label = label
        self.source = source
        self.target = target
        self.color = color
        self.opacity = opacity
        self.width = width
        self.force = force


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
                      .replace("$nodeFontFamily", node_label_font_family)
                      .replace("$nodeFontSize", node_label_font_size)
                      .replace("$nodeFontColor", node_label_color)
                      .replace("$linkFontFamily", link_label_font_family)
                      .replace("$linkFontSize", link_label_font_size)
                      .replace("$linkFontColor", link_label_color)
                      .replace("$linkForce", str(link_force))
                      .replace("$backgroundColor", background_color))
        self._width = width
        self._height = height
        self.show_arrows = show_arrows

        self._nodes: List[Node] = []
        self._edges: List[Edge] = []

        self._edge_id_i = 0

    def node(self, node_id: str) -> Node:
        n = Node(node_id)
        self._nodes.append(n)
        return n

    def edge(self, source_id: str, target_id: str) -> Edge:
        edge = Edge(source_id, target_id)
        edge.id = self._edge_id_i
        self._edge_id_i += 1
        self._edges.append(edge)
        return edge

    def _render_data(self) -> str:
        r = self._html

        nodes = [{
            "id": n.id,
            "label": n.label,
            "tooltip": n.tooltip,
            "color": n.color,
            "level": n.level,
            "radius": n.radius,
            "stroke": n.stroke_color,
            "stroke_width": n.stroke_width
        } for n in self._nodes]

        links = [{
            "id": l.id,
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
