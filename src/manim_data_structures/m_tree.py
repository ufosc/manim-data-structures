import random
from collections import defaultdict
from copy import copy
from typing import Dict, Hashable, List, Tuple

import manim
import networkx as nx
import numpy as np
from manim import *

# def _tree_layout_ltr(
#         T: nx.classes.graph.Graph,
#         root_vertex: Hashable | None,
#         scale: float | tuple | None = 2.0,
#         vertex_spacing: tuple | None = None,
#         orientation: str = "down",
#         children: dict[Hashable, list] = None
# ):
#     if not nx.is_tree(T):
#         raise ValueError("The tree layout must be used with trees")
#     if root_vertex is None:
#         raise ValueError("The tree layout requires the root_vertex parameter")
#
#     # The following code is SageMath's tree layout implementation, taken from
#     # https://github.com/sagemath/sage/blob/cc60cfebc4576fed8b01f0fc487271bdee3cefed/src/sage/graphs/graph_plot.py#L1447
#
#     # Always make a copy of the children because they get eaten
#     stack = [list(children[root_vertex]).copy()]
#     stick = [root_vertex]
#     parent = {u: root_vertex for u in children[root_vertex]}
#     pos = {}
#     obstruction = [0.0] * len(T)
#     orientation = -1 if orientation == "down" else 1
#
#     def slide(v, dx):
#         """
#         Shift the vertex v and its descendants to the right by dx.
#         Precondition: v and its descendents have already had their
#         positions computed.
#         """
#         level = [v]
#         while level:
#             nextlevel = []
#             for u in level:
#                 x, y = pos[u]
#                 x += dx
#                 obstruction[y] = max(x + 1, obstruction[y])
#                 pos[u] = x, y
#                 nextlevel += children[u]
#             level = nextlevel
#
#     while stack:
#         curr_children = stack[-1]
#         if not curr_children:
#             p = stick.pop()
#             stack.pop()
#             cp = children[p]
#             y = orientation * len(stack)
#             if not cp:
#                 x = obstruction[y]
#                 pos[p] = x, y
#             else:
#                 x = sum(pos[c][0] for c in cp) / float(len(cp))
#                 pos[p] = x, y
#                 ox = obstruction[y]
#                 if x < ox:
#                     slide(p, ox - x)
#                     x = ox
#             obstruction[y] = x + 1
#             continue
#
#         t = curr_children.pop()
#         pt = parent[t]
#
#         ct = [u for u in list(T.neighbors(t)) if u != pt]
#         for c in ct:
#             parent[c] = t
#         children[t] = copy(ct)
#
#         stack.append(ct)
#         stick.append(t)
#
#     # the resulting layout is then rescaled again to fit on Manim's canvas
#
#     x_min = min(pos.values(), key=lambda t: t[0])[0]
#     x_max = max(pos.values(), key=lambda t: t[0])[0]
#     y_min = min(pos.values(), key=lambda t: t[1])[1]
#     y_max = max(pos.values(), key=lambda t: t[1])[1]
#     center = np.array([x_min + x_max, y_min + y_max, 0]) / 2
#     height = y_max - y_min
#     width = x_max - x_min
#     if vertex_spacing is None:
#         if isinstance(scale, (float, int)) and (width > 0 or height > 0):
#             sf = 2 * scale / max(width, height)
#         elif isinstance(scale, tuple):
#             if scale[0] is not None and width > 0:
#                 sw = 2 * scale[0] / width
#             else:
#                 sw = 1
#
#             if scale[1] is not None and height > 0:
#                 sh = 2 * scale[1] / height
#             else:
#                 sh = 1
#
#             sf = np.array([sw, sh, 0])
#         else:
#             sf = 1
#     else:
#         sx, sy = vertex_spacing
#         sf = np.array([sx, sy, 0])
#     return {v: (np.array([x, y, 0]) - center) * sf for v, (x, y) in pos.items()}


def _tree_layout_ltr(
    T: nx.classes.graph.Graph,
    root_vertex: Hashable | None,
    scale: float | tuple | None = 2.0,
    vertex_spacing: tuple | None = None,
    orientation: str = "down",
    children: dict[Hashable, list] = None,
):
    """
    Arranges the tree from left to right
    """
    curr_children = [list(children[root_vertex]).copy()]
    curr_parent = [root_vertex]
    pos = {}
    x_min = min(pos.values(), key=lambda t: t[0])[0]
    x_max = max(pos.values(), key=lambda t: t[0])[0]
    y_min = min(pos.values(), key=lambda t: t[1])[1]
    y_max = max(pos.values(), key=lambda t: t[1])[1]
    center = np.array([x_min + x_max, y_min + y_max, 0]) / 2
    sx, sy = vertex_spacing
    sf = np.array([sx, sy, 0])
    return {v: (np.array([x, y, 0]) - center) * sf for v, (x, y) in pos.items()}


class Tree(VMobject):
    """Computer Science Tree Data Structure"""

    __graph: Graph
    __parents: list
    __children: dict[Hashable, list] = defaultdict(list)

    def __init__(
        self, vmobjects: List[Mobject], parents: List[Hashable], edge_buff=0.0, **kwargs
    ):
        super().__init__(**kwargs)
        self.__parents = parents
        vertices: List[Hashable] = []
        edges: List[Tuple[Hashable, Hashable]] = []
        mobjects: Dict[int, Mobject] = {}
        for i, node in enumerate(vmobjects):
            mobjects[i] = node
            vertices.append(i)
        for i, parent in enumerate(parents):
            if parent is not None:
                edges.append((parent, i))
        for parent, child in edges:
            self.__children[parent].append(child)

        self.__graph = Graph(
            vertices,
            edges,
            vertex_mobjects=mobjects,
            layout="tree",
            root_vertex=0,
            layout_scale=len(vmobjects) * 0.5,
            edge_config={"stroke_width": 1, "stroke_color": WHITE},
        )
        # self.__graph.change_layout(
        #     layout=_tree_layout_ltr(children=self.__children, root_vertex=0, T=self.__graph._graph),
        #     layout_scale=len(self.__parents) * 0.5)
        if edge_buff is not None:
            for (u, v), edge in self.__graph.edges.items():
                buff_vec = (
                    edge_buff
                    * (self.__graph[u].get_center() - self.__graph[v].get_center())
                    / np.linalg.norm(
                        self.__graph[u].get_center() - self.__graph[v].get_center()
                    )
                )
                edge.put_start_and_end_on(
                    self.__graph[u].get_center() - buff_vec,
                    self.__graph[v].get_center() + buff_vec,
                )

        def update_edges(graph: Graph):
            """Updates edges of graph"""
            for (u, v), edge in graph.edges.items():
                buff_vec = (
                    edge_buff
                    * (graph[u].get_center() - graph[v].get_center())
                    / np.linalg.norm(graph[u].get_center() - graph[v].get_center())
                )
                edge.put_start_and_end_on(
                    graph[u].get_center() - buff_vec, graph[v].get_center() + buff_vec
                )

        self.__graph.updaters.clear()
        self.__graph.updaters.append(update_edges)
        self.add(self.__graph)

    def __setitem__(self, __index: Hashable, __value: Mobject) -> None:
        """Sets the value of a node in the tree"""
        node_center = self.__graph[__index].get_center()
        node_parent = self.__parents[__index]
        self.__graph.remove_vertices(__index)
        self.__graph.add_vertices(
            __index,
            vertex_mobjects={__index: __value},
            positions={__index: node_center},
        )
        self.__graph.add_edges((node_parent, __index))
        for i, parent in enumerate(self.__parents):
            if parent == __index:
                self.__graph.add_edges((__index, i))

    def __insert__(
        self, __parent: Hashable, __value: Mobject, __index: Hashable = 0
    ) -> None:
        self.__graph.add_vertices(__index, vertex_mobjects={__index: __value})
        self.__graph.add_edges((__parent, __index))
        self.__graph.change_layout(
            layout=_tree_layout_ltr(
                children=self.__children,
                root_vertex=0,
                T=self.__graph._graph,
                vertex_spacing=(1, 1),
            ),
            layout_scale=len(self.__parents) * 0.5,
        )


if __name__ == "__main__":

    class TestScene(Scene):
        def construct(self):
            #  make a parent list for a tree
            pars = [None, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
            #  make a list of mobjects random integers
            nodes = [Integer(2 * x) for x in range(len(p))]
            tree = Tree(nodes, pars, edge_buff=0.4)
            tree.__setitem__(8, Integer(1))
            self.play(Create(tree))
            self.wait()
            # graph = manim.Graph([0, 2], [(0, 2)], root_vertex=0, layout='tree', vertex_type=Integer)
            # graph.add_vertices(1, vertex_type=Integer)
            # graph.add_vertices(3, vertex_type=Integer)
            # graph.add_edges((0, 1))
            # graph.add_edges((1, 3))
            # graph.change_layout('tree', root_vertex=0)
            # self.play(Create(graph))
            # self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "low_quality"
    TestScene().render(preview=True)
