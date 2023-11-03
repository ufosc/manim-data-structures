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
    __vertex_type: Callable[..., Mobject]

    # __parents: list
    # __children: dict[Hashable, list] = defaultdict(list)

    def __init__(
        self,
        vertices: list[Any],
        edges: list[tuple[int, int]],
        vertex_type: Callable[..., Mobject],
        edge_buff=0.4,
        layout="tree",
        layout_config={"vertex_spacing": (-1, 1)},
        root_vertex=0,
        **kwargs
    ):
        super().__init__(**kwargs)
        vertex_mobjects = {i: vertex_type(v) for i, v in enumerate(vertices)}
        self.__layout_config = layout_config
        self.__layout_scale = len(vertices) * 0.5
        self.__vertex_type = vertex_type

        self._graph = Graph(
            list(range(len(vertices))),
            edges,
            vertex_mobjects=vertex_mobjects,
            layout=layout,
            root_vertex=0,
            layout_config=self.__layout_config,
            layout_scale=len(vertices) * 0.5,
            edge_config={"stroke_width": 1, "stroke_color": WHITE},
        )

        # if edge_buff is not None:
        #     for (u, v), edge in self.__graph.edges.items():
        #         buff_vec = (
        #             edge_buff
        #             * (self.__graph[u].get_center() - self.__graph[v].get_center())
        #             / np.linalg.norm(
        #                 self.__graph[u].get_center() - self.__graph[v].get_center()
        #             )
        #         )
        #         edge.put_start_and_end_on(
        #             self.__graph[u].get_center() - buff_vec,
        #             self.__graph[v].get_center() + buff_vec,
        #         )

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

    # def __setitem__(self, __index: Hashable, __value: Mobject) -> None:
    #     """Sets the value of a node in the tree"""
    #     node_center = self.__graph[__index].get_center()
    #     node_parent = self.__parents[__index]
    #     self.__graph.remove_vertices(__index)
    #     self.__graph.add_vertices(
    #         __index,
    #         vertex_mobjects={__index: __value},
    #         positions={__index: node_center},
    #     )
    #     self.__graph.add_edges((node_parent, __index))
    #     for i, parent in enumerate(self.__parents):
    #         if parent == __index:
    #             self.__graph.add_edges((__index, i))

    def __insert__(self, parent_index: int, value: Any) -> None:
        """Inserts a node into the tree"""
        self.__graph.add_vertices(
            len(self.__graph.vertices),
            vertex_mobjects={len(self.__graph.vertices): self.__vertex_type(value)},
        )
        self.__graph.add_edges((parent_index, len(self.__graph.vertices) - 1))
        self.__graph.change_layout(
            "tree",
            root_vertex=0,
            layout_config=self.__layout_config,
            layout_scale=self.__layout_scale,
        )
        # self.__graph.update()

    # def __animate_insert__(self, ):
    def __remove__(self, index: int) -> None:
        """Removes a node from the tree"""
        self.__graph.remove_vertices(index)
        self.__graph.change_layout(
            "tree",
            root_vertex=0,
            layout_config=self.__layout_config,
            layout_scale=self.__layout_scale,
        )
        self.__graph.update()


if __name__ == "__main__":

    class TestScene(Scene):
        def construct(self):
            #  make a parent list for a tree
            tree = Tree([0, 1, 2, 3, 5], [(0, 1), (0, 2), (1, 3), (1, 4)], Integer)
            self.play(Create(tree))
            # for i in range(5):
            #     self.wait()
            #     tree.__insert__(2, i + 5)
            tree.__remove__(2)
            self.play(tree.animate)
            self.wait()
            # self.play(tree._Tree__graph.vertices[0].animate.shift(UP * 2))
            # graph.change_layout('tree', root_vertex=0)
            # self.play(Create(graph))
            # self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "low_quality"
    TestScene().render(preview=True)
