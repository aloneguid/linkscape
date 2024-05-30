from linkscape.network import ForceDirectedGraph, Node, Link
from random import randint

save_path = "canvas.html"


def test_simplest():
    g = ForceDirectedGraph(800, 200, link_force=0.5)

    nodes = ["dev", "pre-prod", "prod", "developers", "testers", "managers"]
    colours = ["green", "green", "green", "blue", "blue", "blue"]

    for n, c in zip(nodes, colours):
        g.add_nodes(Node(n, n, color=c))

    # link process
    g.add_links(Link("dev", "pre-prod", force=0.1))
    g.add_links(Link("pre-prod", "prod", force=0.1))

    # link involved
    g.add_links(Link("developers", "dev"))
    g.add_links(Link("developers", "pre-prod"))
    g.add_links(Link("testers", "pre-prod"))
    g.add_links(Link("managers", "prod"))

    g.save(save_path)
    print(g._repr_html_())


def test_labels_and_strokes():
    g = ForceDirectedGraph()
    g.add_nodes(Node("one", radius=10))
    g.add_nodes(Node("two", radius=20))
    g.add_nodes(Node("three", radius=20))
    g.add_nodes(Node("red border", stroke_color="red", stroke_width=5))
    g.save(save_path)


def test_multi_level():
    g = ForceDirectedGraph(1000, 1000, x_levels=3, collision_radius=1, link_force=0)

    def nid(id: int, lvl: int) -> str:
        return f"node_L{lvl}_I{id}"

    def add_lvl(lvl: int, color: str):
        g.add_nodes(*[Node(nid(i, lvl), label="x3", radius=randint(1, 20), color=color, level=lvl) for i in range(0, 100)])

    # add nodes for levels
    add_lvl(1, "red")
    add_lvl(2, "green")
    add_lvl(3, "blue")

    # interlink them randomly

    def interlink(from_lvl: int, to_lvl: int, color: str):
        for i in range(0, 10):
            g.add_links(Link(nid(i, from_lvl), nid(randint(0, 100), to_lvl), color=color))

    interlink(1, 2, "green")
    interlink(2, 3, "blue")

    g.save(save_path)


def test_twitter_nel():
    path = "c:\\tmp\\TWITTER-Real-Graph-Partial.nel"
    with open(path, "r") as reader:
        lines = reader.readlines()

    g = ForceDirectedGraph(1000, 1000, collision_radius=40)

    # n 1 apple
    # n 2 store
    # n 3 buy
    # n 4 mac
    # e 1 2 3.034013E-4
    # e 3 4 1.6500772E-4
    # e 3 2 3.5130675E-4
    # g 2191352508 56

    mp = dict()
    for line in lines[:10]:
        pts = line.split(" ")
        if len(pts) >= 3:
            if pts[0] == "n":
                id = pts[1]
                name = pts[2]
                g.add_nodes(Node(id, name, f"id: {id}, name: {name}"))
                mp[id] = name
            if pts[0] == "e":
                id_from = pts[1]
                id_to = pts[2]
                label = pts[3]
                g.add_links(Link(id_from, id_to, opacity=0.5, label=label))
        else:
            mp = dict()


    g.save(save_path)

    print(len(lines))


