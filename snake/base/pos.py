from snake.base.direc import Direc


class Pos:
    """二维平面上的整数坐标

    坐标系的原点在左上角，x轴向下延伸，y轴向右延伸。
    """

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __str__(self):
        return f"Pos({self._x},{self._y})"

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self._x == other.x and self._y == other.y
        return NotImplemented

    def __pos__(self):
        return Pos(self._x, self._y)

    def __neg__(self):
        return Pos(-self._x, -self._y)

    def __add__(self, other):
        if isinstance(self, other.__class__):
            return Pos(self._x + other.x, self._y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(self, other.__class__):
            return self + (-other)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def manhattan_dist(p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def direc_to(self, adj_pos):
        """返回相邻位置相对于当前位置的方向"""
        if self._x == adj_pos.x:
            diff = self._y - adj_pos.y
            if diff == 1:
                return Direc.LEFT
            if diff == -1:
                return Direc.RIGHT
        elif self._y == adj_pos.y:
            diff = self._x - adj_pos.x
            if diff == 1:
                return Direc.UP
            if diff == -1:
                return Direc.DOWN
        return Direc.NONE

    def adj(self, direc):
        """返回指定方向上的相邻位置"""
        if direc == Direc.LEFT:
            return Pos(self._x, self._y - 1)
        elif direc == Direc.RIGHT:
            return Pos(self._x, self._y + 1)
        elif direc == Direc.UP:
            return Pos(self._x - 1, self._y)
        elif direc == Direc.DOWN:
            return Pos(self._x + 1, self._y)
        else:
            return None

    def all_adj(self):
        """返回所有相邻位置的列表"""
        adjs = []
        for direc in Direc:
            if direc != Direc.NONE:
                adjs.append(self.adj(direc))
        return adjs

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val