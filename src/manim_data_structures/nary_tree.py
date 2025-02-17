from typing import Any, Callable, Hashable

import networkx as nx
import numpy as np
from m_tree import Tree
from manim import Mobject


def _nary_layout(
    T: nx.classes.graph.Graph,
    vertex_spacing: tuple | None = None,
    n: int | None = None,
):
    if not n:
        raise ValueError("the n-ary tree layout requires the n parameter")
    if not nx.is_tree(T):
        raise ValueError("The tree layout must be used with trees")

    max_height = NaryTree.calc_loc(max(T), n)[1]

    def calc_pos(x, y):
        """
        Scales the coordinates to the desired spacing
        """
        return (x - (n**y - 1) / 2) * vertex_spacing[0] * n ** (
            max_height - y
        ), y * vertex_spacing[1]

    return {
        i: np.array([x, y, 0])
        for i, (x, y) in ((i, calc_pos(*NaryTree.calc_loc(i, n))) for i in T)
    }


class NaryTree(Tree):
    def __init__(
        self,
        nodes: dict[int, Any],
        num_child: int,
        vertex_type: Callable[..., Mobject],
        edge_buff=0.4,
        layout_config=None,
        **kwargs
    ):
        if layout_config is None:
            layout_config = {"vertex_spacing": (-1, 1)}
        self.__layout_config = layout_config
        self.num_child = num_child

        edges = [(self.get_parent(e), e) for e in nodes if e != 0]
        super().__init__(nodes, edges, vertex_type, edge_buff, **kwargs)
        dict_layout = _nary_layout(self._graph._graph, n=num_child, **layout_config)
        self._graph.change_layout(dict_layout)

    @staticmethod
    def calc_loc(i, n):
        """
        Calculates the coordinates in terms of the shifted level order x position and level height
        """
        if n == 1:
            return 1, i + 1
        height = int(np.emath.logn(n, i * (n - 1) + 1))
        node_shift = (1 - n**height) // (1 - n)
        return i - node_shift, height

    @staticmethod
    def calc_idx(loc, n):
        """
        Calculates the index from the coordinates
        """
        x, y = loc
        if n == 1:
            return y - 1

        return int(x + (1 - n**y) // (1 - n))

    def get_parent(self, idx):
        """
        Returns the index of the parent of the node at the given index
        """
        x, y = NaryTree.calc_loc(idx, self.num_child)
        new_loc = x // self.num_child, y - 1
        return NaryTree.calc_idx(new_loc, self.num_child)

    def insert_node(self, node: Any, index: Hashable):
        """Inserts a node into the graph"""
        res = super().insert_node(node, (self.get_parent(index), index))
        dict_layout = _nary_layout(
            self._graph._graph, n=self.num_child, **self.__layout_config
        )
        self._graph.change_layout(dict_layout)
        self.update()
        return res


if __name__ == "__main__":
    from manim import *

    class TestScene(Scene):
        def construct(self):
            tree = NaryTree(
                {0: 0, 1: 1, 4: 4},
                num_child=2,
                vertex_type=Integer,
                layout_config={"vertex_spacing": (1, -1)},
            )
            # tree._graph.change_layout(root_vertex=0, layout_config=tree._Tree__layout_config,
            #                           layout_scale=tree._Tree__layout_scale)
            self.play(Create(tree))
            self.wait()
            tree.insert_node(3, 3)
            self.wait()
            tree.remove_node(4)
            self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "low_quality"
    TestScene().render(preview=True)
