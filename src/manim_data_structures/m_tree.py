import random
from collections import defaultdict
from copy import copy
from typing import Any, Callable, Dict, Hashable, List, Tuple

import numpy as np
from manim import *
from manim import WHITE, Graph, Mobject, VMobject


class Tree(VMobject):
    """Computer Science Tree Data Structure"""

    _graph: Graph
    __layout_config: dict
    __layout_scale: float
    __layout: str | dict
    __vertex_type: Callable[..., Mobject]

    # __parents: list
    # __children: dict[Hashable, list] = defaultdict(list)

    def __init__(
        self,
        nodes: dict[int, Any],
        edges: list[tuple[int, int]],
        vertex_type: Callable[..., Mobject],
        edge_buff=0.4,
        layout="tree",
        layout_config={"vertex_spacing": (-1, 1)},
        root_vertex=0,
        **kwargs
    ):
        super().__init__(**kwargs)
        vertex_mobjects = {k: vertex_type(v) for k, v in nodes.items()}
        self.__layout_config = layout_config
        self.__layout_scale = len(nodes) * 0.5
        self.__layout = layout
        self.__vertex_type = vertex_type
        self._graph = Graph(
            list(nodes),
            edges,
            vertex_mobjects=vertex_mobjects,
            layout=layout,
            root_vertex=0,
            layout_config=self.__layout_config,
            layout_scale=len(nodes) * 0.5,
            edge_config={"stroke_width": 1, "stroke_color": WHITE},
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

        self._graph.updaters.clear()
        self._graph.updaters.append(update_edges)
        self.add(self._graph)

    def insert_node(self, node: Any, edge: tuple[Hashable, Hashable]):
        """Inserts a node into the graph as (parent, node)"""
        self._graph.add_vertices(
            edge[1], vertex_mobjects={edge[1]: self.__vertex_type(node)}
        )
        self._graph.add_edges(edge)

    def remove_node(self, node: Hashable):
        """Removes a node from the graph"""
        self._graph.remove_vertices(node)


if __name__ == "__main__":

    class TestScene(Scene):
        def construct(self):
            #  make a parent list for a tree
            tree = Tree({0: 0, 1: 1, 2: 2, 3: 3}, [(0, 1), (0, 2), (1, 3)], Integer)
            tree.insert_node(4, (2, 4))
            self.play(Create(tree))
            self.play(tree.animate)
            self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "low_quality"
    TestScene().render(preview=True)
