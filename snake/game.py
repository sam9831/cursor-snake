import errno
import os
from enum import Enum, unique

from snake.base import Direc, Map, PointType, Pos, Snake
from snake.gui import GameWindow

# 添加解决方案名称到globals()
from snake.solver import GreedySolver


@unique
class GameMode(Enum):
    NORMAL = 0  # 带GUI的AI


class GameConf:
    def __init__(self):
        """初始化默认配置"""

        # 游戏模式
        self.mode = GameMode.NORMAL

        # 解决方案
        self.solver_name = "GreedySolver"  # 解决方案的类名

        # 尺寸
        self.map_rows = 8
        self.map_cols = self.map_rows
        self.map_width = 160  # 像素
        self.map_height = self.map_width
        self.info_panel_width = 155  # 像素
        self.window_width = self.map_width + self.info_panel_width
        self.window_height = self.map_height
        self.grid_pad_ratio = 0.25

        # 开关
        self.show_grid_line = False
        self.show_info_panel = True

        # 延迟
        self.interval_draw = 50  # 毫秒
        self.interval_draw_max = 200  # 毫秒

        # 颜色
        self.color_bg = "#000000"
        self.color_txt = "#F5F5F5"
        self.color_line = "#424242"
        self.color_wall = "#F5F5F5"
        self.color_food = "#FFF59D"
        self.color_head = "#F5F5F5"
        self.color_body = "#F5F5F5"

        # 初始蛇
        self.init_direc = Direc.RIGHT
        self.init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        self.init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3

        # 字体
        self.font_info = ("Arial", 9)

        # 信息
        self.info_str = (
            "<w/a/s/d>: 蛇的方向\\n"
            "<空格>: 暂停/继续\\n"
            "<r>: 重启    <esc>: 退出\\n"
            "-----------------------------------\\n"
            "状态: %s\\n"
            "回合: %d   步数: %d\\n"
            "长度: %d/%d (" + str(self.map_rows) + "x" + str(self.map_cols) + ")\\n"
            "-----------------------------------"
        )
        self.info_status = ["进食中", "死亡", "满了"]


class Game:
    def __init__(self, conf):
        self._conf = conf
        self._map = Map(conf.map_rows + 2, conf.map_cols + 2)
        self._snake = Snake(
            self._map, conf.init_direc, conf.init_bodies, conf.init_types
        )
        self._pause = False
        self._solver = globals()[self._conf.solver_name](self._snake)
        self._episode = 1
        self._init_log_file()

    @property
    def snake(self):
        return self._snake

    @property
    def episode(self):
        return self._episode

    def run(self):
        window = GameWindow(
            "贪吃蛇",
            self._conf,
            self._map,
            self,
            self._on_exit,
            (
                ("<w>", lambda e: self._update_direc(Direc.UP)),
                ("<a>", lambda e: self._update_direc(Direc.LEFT)),
                ("<s>", lambda e: self._update_direc(Direc.DOWN)),
                ("<d>", lambda e: self._update_direc(Direc.RIGHT)),
                ("<r>", lambda e: self._reset()),
                ("<space>", lambda e: self._toggle_pause()),
            ),
        )
        window.show(self._game_main_normal)

    def _game_main_normal(self):
        if not self._map.has_food():
            self._map.create_rand_food()

        if self._pause or self._is_episode_end():
            return

        self._update_direc(self._solver.next_direc())

        if self._snake.direc_next != Direc.NONE:
            self._write_logs()

        self._snake.move()

        if self._is_episode_end():
            self._write_logs()  # 记录最后一步

    def _update_direc(self, new_direc):
        self._snake.direc_next = new_direc
        if self._pause:
            self._snake.move()

    def _toggle_pause(self):
        self._pause = not self._pause

    def _is_episode_end(self):
        return self._snake.dead or self._map.is_full()

    def _reset(self):
        self._snake.reset()
        self._episode += 1

    def _on_exit(self):
        if self._log_file:
            self._log_file.close()
        if self._solver:
            self._solver.close()

    def _init_log_file(self):
        try:
            os.makedirs("logs")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            self._log_file = None
            self._log_file = open("logs/snake.log", "w", encoding="utf-8")
        except FileNotFoundError:
            if self._log_file:
                self._log_file.close()

    def _write_logs(self):
        self._log_file.write(
            f"[ 回合 {self._episode} / 步数 {self._snake.steps} ]\\n"
        )
        for i in range(self._map.num_rows):
            for j in range(self._map.num_cols):
                pos = Pos(i, j)
                t = self._map.point(pos).type
                if t == PointType.EMPTY:
                    self._log_file.write("  ")
                elif t == PointType.WALL:
                    self._log_file.write("# ")
                elif t == PointType.FOOD:
                    self._log_file.write("F ")
                elif (
                    t == PointType.HEAD_L
                    or t == PointType.HEAD_U
                    or t == PointType.HEAD_R
                    or t == PointType.HEAD_D
                ):
                    self._log_file.write("H ")
                elif pos == self._snake.tail():
                    self._log_file.write("T ")
                else:
                    self._log_file.write("B ")
            self._log_file.write("\\n")
        self._log_file.write(
            f"[ 上一步/下一步方向: {self._snake.direc}/{self._snake.direc_next} ]\\n"
        )
        self._log_file.write("\\n")