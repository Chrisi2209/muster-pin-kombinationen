import logging
import os
from typing import List, Tuple, Dict, Optional, Callable
import sys
sys.path.insert(0, "C:\Programmieren\VS_Code\pythonAlgorithmusÜbungen")
if True:
    from kap3.csp import Node, Queue


def setup_logging(name: str) -> logging.Logger:
    path_to_dir = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "logs"))
    path_to_log = os.path.abspath(os.path.join(path_to_dir, f"{name}.log"))

    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)

    file_handler = logging.FileHandler(path_to_log)
    file_handler.setFormatter(logging.Formatter(
        "%(levelname)-7s %(processName)s %(threadName)s %(asctime)s %(funcName)s: %(message)s"))

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    return logger


Coordinate = Tuple[int, int]


def count_bfs(successors: Callable, goal_test: Callable, initial: Coordinate) -> Tuple[Optional[Node], int]:
    explored: set = {initial}
    frontier: Queue = Queue()

    frontier.push(Node(initial, None))

    counter: int = 0
    while not frontier.empty:
        current_node: Node = frontier.pop()

        add: int = 1
        for _ in range(4):
            if current_node.parent == None:
                add = 0
                break

        counter += add

        if goal_test(current_node.state):
            return current_node, counter

        childs: list[Coordinate] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node))

    return None, counter


def successors(c: Coordinate):
    succ: List[Coordinate] = []
    if c[0] + 1 < 3:
        succ.append((c[0] + 1, c[1]))
    if c[0] - 1 >= 0:
        succ.append((c[0] - 1, c[1]))
    if c[1] + 1 < 3:
        succ.append((c[0], c[1] + 1))
    if c[1] - 1 >= 0:
        succ.append((c[0], c[1] - 1))

    return succ


def main():
    count: int = count_bfs(successors, lambda x: False, (0, 0))[1] * 4
    print(f"count vertecies: {count}")
    count += count_bfs(successors, lambda x: False, (1, 0))[1] * 4
    print(f"count vertecies + edges : {count}")
    count += count_bfs(successors, lambda x: False, (1, 1))[1]

    print(f"final count: {count}")


if __name__ == "__main__":
    main()
