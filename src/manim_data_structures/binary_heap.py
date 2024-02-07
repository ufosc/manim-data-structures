from m_nary_tree import N_ary_tree, _nary_layout
from manim import *
from manim import Create, Integer, Scene


class BinaryHeap(N_ary_tree):

    size: int
    lst: list[int]
    compare: Callable[[int, int], bool]

    def __init__(self, compare):
        super().__init__(
            {0: 11},
            num_child=2,
            vertex_type=Integer,
            layout_config={"vertex_spacing": (1, -1)},
        )
        self.size = 1
        self.lst = [11]
        self.compare = compare

    def rebuild_tree(self):
        super().__init__(
            {i: self.lst[i] for i in range(len(self.lst))},
            num_child=2,
            vertex_type=Integer,
            layout_config={"vertex_spacing": (1, -1)},
        )

    def push(self, val: int):
        self.lst.append(val)
        self.insert_node(val, self.size)
        self.size += 1
        cur = self.size - 1
        par = (cur - 1) // 2
        while self.compare(self.lst[cur], self.lst[par]):
            self.lst[cur], self.lst[par] = self.lst[par], self.lst[cur]
            self.rebuild_tree()
            cur = par
            if cur == 0:
                break
            par = (cur - 1) // 2

    def pop(self):
        root_val = self.lst[0]
        self.lst[0] = self.lst[-1]
        self.lst.pop()
        self.size -= 1
        cur = 0
        while True:
            mn_ind = cur
            left = 2 * cur + 1
            if left < len(self.lst) and self.compare(self.lst[left], self.lst[mn_ind]):
                mn_ind = left
            right = 2 * cur + 2
            if right < len(self.lst) and self.compare(
                self.lst[right], self.lst[mn_ind]
            ):
                mn_ind = right
            if mn_ind == cur:
                break
            self.lst[mn_ind], self.lst[cur] = self.lst[cur], self.lst[mn_ind]
            self.rebuild_tree()
            cur = mn_ind
        return root_val


if __name__ == "__main__":

    class TestScene(Scene):
        def construct(self):
            heap = BinaryHeap(lambda x, y: x < y)
            self.add(heap)
            self.wait()
            heap.push(10)
            self.wait()
            heap.push(7)
            self.wait()
            heap.push(17)
            self.wait()
            heap.push(4)
            self.wait()
            heap.pop()
            self.wait()
            heap.pop()
            self.wait()

    config.preview = True
    config.renderer = "cairo"
    config.quality = "low_quality"
    TestScene().render(preview=True)
