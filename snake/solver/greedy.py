from snake.base.pos import Pos
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class GreedySolver(BaseSolver):
    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)

    def next_direc(self):
        # 创建虚拟蛇
        s_copy, m_copy = self.snake.copy()

        # 步骤 1：找到通向食物的最短路径
        self._path_solver.snake = self.snake
        path_to_food = self._path_solver.shortest_path_to_food()

        if path_to_food:
            # 步骤 2：沿着找到的路径移动虚拟蛇
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]

            # 步骤 3：检查虚拟蛇移动后是否可以找到通往尾巴的最长路径
            self._path_solver.snake = s_copy
            path_to_tail = self._path_solver.longest_path_to_tail()
            if len(path_to_tail) > 1:
                return path_to_food[0]

        # 步骤 4：如果无法安全吃食物，尝试找到通往尾巴的最长路径
        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        # 步骤 5：如果以上都失败，选择远离食物的方向
        head = self.snake.head()
        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.manhattan_dist(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direc_to(adj)
        return direc