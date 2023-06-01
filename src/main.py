from generic_search import Queue, Node
import logging
import os
from typing import List, Tuple, Dict, Optional, Callable
import sys
sys.path.insert(0, "C:\Programmieren\VS_Code\pythonAlgorithmusÜbungen")


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


def count_bfs(successors: Callable, initial: Coordinate) -> Tuple[Optional[Node], int]:
    frontier: Queue = Queue()

    frontier.push(Node(initial, None))

    counter: int = 0
    while not frontier.empty:
        current_node: Node = frontier.pop()
        history = current_node.history_of_states

        counter += 1 if len(history) >= 4 else 0
        if len(history) > 9:
            raise Exception()

        childs: list[Coordinate] = successors(current_node.state)

        for child in childs:
            if child not in history:
                # top left to bottom right
                if current_node.state == (0, 0) and child == (2, 2) and (1, 1) not in history:
                    continue
                # bottom right to top left
                if current_node.state == (2, 2) and child == (0, 0) and (1, 1) not in history:
                    continue
                # top right to bottom left
                if current_node.state == (2, 0) and child == (0, 2) and (1, 1) not in history:
                    continue
                # bottom left to top right
                if current_node.state == (0, 2) and child == (2, 0) and (1, 1) not in history:
                    continue
                # rows
                if current_node.state[0] == 0 and child[0] == 2 and current_node.state[1] == child[1] and (1, child[1]) not in history:
                    continue
                # columns
                if current_node.state[1] == 0 and child[1] == 2 and current_node.state[0] == child[0] and (child[0], 1) not in history:
                    continue
                # rows inverse
                if current_node.state[0] == 2 and child[0] == 0 and current_node.state[1] == child[1] and (1, child[1]) not in history:
                    continue
                # columns inverse
                if current_node.state[1] == 2 and child[1] == 0 and current_node.state[0] == child[0] and (child[0], 1) not in history:
                    continue

                frontier.push(Node(child, current_node))

    return None, counter


def successors(c: Coordinate):
    return [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


def main():
    count: int = count_bfs(successors, (0, 0))[1] * 4
    print(f"count vertecies: {count}")
    count += count_bfs(successors, (1, 0))[1] * 4
    print(f"count vertecies + edges : {count}")
    count += count_bfs(successors, (1, 1))[1]

    print(f"final count: {count}")


if __name__ == "__main__":
    main()
