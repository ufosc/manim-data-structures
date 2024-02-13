import operator as op
import random
from collections import defaultdict
from copy import copy
from functools import partialmethod, reduce
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
        return self

    def insert_node2(self, node: Any, edge: tuple[Hashable, Hashable]):
        """Inserts a node into the graph as (parent, node)"""
        self._graph.change_layout(
            self.__layout,
            layout_scale=self.__layout_scale,
            layout_config=self.__layout_config,
            root_vertex=0,
        )
        for mob in self.family_members_with_points():
            if (mob.get_center() == self._graph[edge[1]].get_center()).all():
                mob.points = mob.points.astype("float")
        return self

    def insert_node3(self, node: Any, edge: tuple[Hashable, Hashable]):
        """Inserts a node into the graph as (parent, node)"""
        self.suspend_updating()
        self.insert_node(node, edge)
        # self.resume_updating()
        self.insert_node2(node, edge)

        return self

    def remove_node(self, node: Hashable):
        """Removes a node from the graph"""
        self._graph.remove_vertices(node)

    # def insert_node2(self):
    #     """Shift by the given vectors.
    #
    #     Parameters
    #     ----------
    #     vectors
    #         Vectors to shift by. If multiple vectors are given, they are added
    #         together.
    #
    #     Returns
    #     -------
    #     :class:`Mobject`
    #         ``self``
    #
    #     See also
    #     --------
    #     :meth:`move_to`
    #     """
    #
    #     total_vector = reduce(op.add, vectors)
    #     for mob in self.family_members_with_points():
    #         mob.points = mob.points.astype("float")
    #         mob.points += total_vector
    #
    #     return self


if __name__ == "__main__":

    class TestScene(Scene):
        def construct(self):
            #  make a parent list for a tree
            tree = Tree({0: 0, 1: 1, 2: 2, 3: 3}, [(0, 1), (0, 2), (1, 3)], Integer)
            self.play(Create(tree))
            self.wait()
            self.play(tree.animate.insert_node3(4, (2, 4)), run_time=0)
            self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "low_quality"
    TestScene().render(preview=True)
