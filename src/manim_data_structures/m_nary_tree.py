from typing import Hashable
from m_tree import Tree
from manim import *
from manim import WHITE, Graph, Mobject, VMobject
import networkx as nx




class N_ary_tree(Tree):
    def __init__(
        self,
        nary_tree_list: list[Any],
        num_child: int,
        vertex_type: Callable[..., Mobject],
        edge_buff=0.4,
        layout_config={"vertex_spacing": (-1, 1)},
        root_vertex=0,
        **kwargs
    ):
        n = num_child
        def n_ary_layout(
            T: nx.classes.graph.Graph,
            root_vertex: Hashable | None,
            scale: float | tuple | None = 2,
            vertex_spacing: tuple | None = None,
            orientation: str = "down",
        ):
            if not n:
                raise ValueError("the n-ary tree layout requires the n parameter")
            if not nx.is_tree(T):
                raise ValueError("The tree layout must be used with trees")
            if root_vertex is None:
                raise ValueError("The tree layout requires the root_vertex parameter")
            def calc_pos(i):
                if n == 1:
                    return (1, i+1)
                k=0
                sum = 0
                while True:
                    sum += n**k
                    if i<sum:
                        return(i-sum + n**k, k+1)
                    else:
                        k += 1
            return {i: np.array([x, y, 0]) for x,y in (calc_pos(i) for i in T)}

        self.num_child = num_child
        height = 1 + int(np.log(len(nary_tree_list) + 1) / np.log(num_child))
        total_vertices = num_child**height - 1
        vertices = list(nary_tree_list)
        edges = [(e // num_child, e + 1) for e in range(len(vertices) - 1)]
        # vertices = vertices + vertices_null
        #
        # vertices = vertices + vertices_null
        print(vertices)

        print(edges)

        super().__init__(
            vertices,
            edges,
            vertex_type,
            edge_buff,
            n_ary_layout,
            layout_config,
            root_vertex,
            **kwargs
        )


if __name__ == "__main__":

    class TestScene(Scene):
        def construct(self):
            #  make a parent list for a tree
            tree = N_ary_tree(
                [0, 1, 2, 3, 4, 5, 6, 7, 244, 4], num_child=3, vertex_type=Integer
            )
            self.play(Create(tree))
            # for i in range(5):
            #     self.wait()
            #     tree.__insert__(2, i + 5)
            # tree.__remove__(2)
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
