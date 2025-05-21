import argparse

from snake.game import Game, GameConf, GameMode


def main():
    dict_solver = {
        "greedy": "GreedySolver",
    }

    dict_mode = {
        "normal": GameMode.NORMAL,
    }

    parser = argparse.ArgumentParser(description="运行贪吃蛇游戏")
    parser.add_argument(
        "-s",
        default="greedy",
        choices=dict_solver.keys(),
        help="用于控制蛇移动的解决方案名称 (默认: greedy)",
    )
    parser.add_argument(
        "-m",
        default="normal",
        choices=dict_mode.keys(),
        help="游戏模式 (默认: normal)",
    )
    args = parser.parse_args()

    conf = GameConf()
    conf.solver_name = dict_solver[args.s]
    conf.mode = dict_mode[args.m]
    print(f"求解器: {conf.solver_name}   模式: {conf.mode}")

    Game(conf).run()


if __name__ == "__main__":
    main()