from typing import Any, Callable, Hashable

import nary_tree as nt
import networkx as nx
from manim import Mobject


class BSTree(nt.NaryTree):

    # BSTree is a NaryTree with num_children=2.
    # BSTree also keeps track of the values of the nodes in the tree with __values
    def __init__(
        self,
        nodes: dict[int, Any],
        vertex_type: Callable[..., Mobject],
        edge_buff=0.4,
        layout_config={"vertex_spacing": (0.6, -0.6)},
        **kwargs
    ):
        self.__values = nodes
        super().__init__(nodes, 2, vertex_type, edge_buff, layout_config, **kwargs)

    def insert_node(self, node: Any):
        """
        Inserts a node into the BST, overriding definition in NaryTree
        """
        # find the place to insert based on BST properties, starts at index=0
        ind = self.find_insertion_index(node)
        # take note of the new node's value
        self.__values[ind] = node
        # insert the new node into the correct position using NaryTree's implementation
        return super().insert_node(node, ind)

    def remove_node(self, node: Any):
        """
        Removes a node with value 'node' from the BST
        """
        ind = -1
        # does not support removing the root
        for k, v in self.__values.items():
            if k != 0 and v == node:
                ind = k
                break
        if ind == -1:
            return
        removal_ind = ind
        # if left child exists
        if ind * 2 + 1 in self.__values:
            ind = ind * 2 + 1
            # find rightmost
            while ind * 2 + 2 in self.__values:
                ind = ind * 2 + 2
            # swap the rightmost down its left
            while ind * 2 + 1 in self.__values:
                self.__values[ind], self.__values[ind * 2 + 1] = (
                    self.__values[ind * 2 + 1],
                    self.__values[ind],
                )
                ind = ind * 2 + 1
            # remove
            self.__values[ind], self.__values[removal_ind] = (
                self.__values[removal_ind],
                self.__values[ind],
            )
            del self.__values[ind]
            self._graph.remove_vertices(ind)
            # get rid of graph
            for vert in self.__values:
                if vert != 0:
                    self._graph.remove_vertices(vert)
            # rebuild; this also makes edges
            for k, v in self.__values.items():
                if k != 0:
                    super().insert_node(v, k)
        # choose right child if left is not present
        elif ind * 2 + 2 in self._graph.vertices:
            ind = ind * 2 + 2
            while ind * 2 + 1 in self.__values:
                ind = ind * 2 + 1
            while ind * 2 + 2 in self.__values:
                self.__values[ind], self.__values[ind * 2 + 2] = (
                    self.__values[ind * 2 + 2],
                    self.__values[ind],
                )
                ind = ind * 2 + 2
            self.__values[ind], self.__values[removal_ind] = (
                self.__values[removal_ind],
                self.__values[ind],
            )
            del self.__values[ind]
            self._graph.remove_vertices(ind)

            for vert in self.__values:
                if vert != 0:
                    self._graph.remove_vertices(vert)
            for k, v in self.__values.items():
                if k != 0:
                    super().insert_node(v, k)
        # just delete it if it has no children
        else:
            self._graph.remove_vertices(removal_ind)
            del self.__values[removal_ind]

    def find_insertion_index(self, node: Any, index=0):
        """
        Finds the position where a value 'node' should be placed
        """
        # if we reach an index not yet created, we are done
        if index not in self._graph.vertices:
            return index
        # otherwise, try to find position at left or right based on value
        if node <= self.__values[index]:
            return self.find_insertion_index(node, index * 2 + 1)
        else:
            return self.find_insertion_index(node, index * 2 + 2)


if __name__ == "__main__":
    from manim import *

    class TestScene(Scene):
        def construct(self):
            tree = BSTree({0: 10}, vertex_type=Integer)
            self.play(Create(tree))
            tree.insert_node(5)
            self.wait()
            tree.insert_node(15)
            self.wait()
            tree.insert_node(20)
            self.wait()
            tree.insert_node(12)
            self.wait()
            tree.insert_node(14)
            self.wait()
            tree.insert_node(13)
            self.wait()
            tree.remove_node(15)
            self.wait()
            self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "high_quality"
    TestScene().render()
