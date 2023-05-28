from __future__ import annotations
from heapq import heappush, heappop
from enum import Enum
from typing import NamedTuple, Optional, Callable, Tuple
import random


class Node:
    def __init__(self, state: MazeLocation, parent: Node, cost = 0, heuristic = 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Stack:
    def __init__(self):
        self._container: list = []

    @property
    def empty(self):
        return not self._container

    def push(self, item):
        self._container.append(item)

    def pop(self):
        return self._container.pop()

class Queue:
    def __init__(self):
        self._container: list = []

    @property
    def empty(self):
        return not self._container

    def push(self, item):
        self._container.append(item)
    
    def pop(self):
        return self._container.pop(0)
    
    def __repr__(self):
        return str(self._container)


class PriorityQueue:
    def __init__(self):
        self._container: list = []
    
    @property
    def empty(self):
        return not self._container

    def push(self, item):
        heappush(self._container, item)

    def pop(self):
        return heappop(self._container)

    def __repr__(self):
        return str(self._container)

class Cell(Enum):
    EMPTY = " "
    BLOCKED = "X"
    PATH = "*"
    START = "S"
    GOAL = "G"

class MazeLocation(NamedTuple):
    row: int
    column: int

class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, sparseness: float = 0.2, 
                 start: MazeLocation = MazeLocation(9, 9), goal: MazeLocation = MazeLocation(0, 0)):
        self._rows = rows
        self._columns = columns
        self._sparseness = sparseness
        self.start = start
        self.goal = goal

        self._grid: list[list[Cell]] = [[Cell.EMPTY for column in range(columns)] for row in range(rows)]
        self._randomly_fill(self._rows, self._columns, self._sparseness)

        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0.0, 1.0) <= sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation):
        return (self.goal == ml)

    def __str__(self):
        output: str = ""
        for row in range(self._rows):
            output += "".join([c.value for c in self._grid[row]]) + "\n"
        return output
    
    def successors(self, ml: MazeLocation):
        locations = []
        if ml.row + 1 < self._rows and self._grid[ml.column][ml.row + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.column][ml.row - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.column + 1][ml.row] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.column - 1][ml.row] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))

        return locations

    def mark(self, path: list[MazeLocation]):
        for ml in path:
            self._grid[ml.column][ml.row] = Cell.PATH
        
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: list[MazeLocation]):
        for ml in path:
            self._grid[ml.column][ml.row] = Cell.EMPTY
        
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

def manhattan_distance(ml2: MazeLocation):
    def inner(ml1):
        return (ml1.column - ml2.column) + (ml1.row - ml2.row)
    return inner

def bfs(successors: Callable, goal_test: Callable, initial: Node) -> Optional[Node]:
    explored: set = {initial}
    frontier: Queue = Queue()

    frontier.push(Node(initial, None))

    while not frontier.empty:
        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node

        childs: list[MazeLocation] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node))

def count_bfs(successors: Callable, goal_test: Callable, initial: Node) -> Tuple[Optional[Node], int]:
    explored: set = {initial}
    frontier: Queue = Queue()

    frontier.push(Node(initial, None))

    counter: int = 0
    while not frontier.empty:
        counter += 1

        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node, counter

        childs: list[MazeLocation] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node))
    
    return None, counter

def dfs(successors: Callable, goal_test: Callable, initial: Node) -> Optional[Node]:
    explored: set = {initial}
    frontier: Stack = Stack()

    frontier.push(Node(initial, None))

    while not frontier.empty:
        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node

        childs: list[MazeLocation] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node))

    return None

def count_dfs(successors: Callable, goal_test: Callable, initial: Node) -> Tuple[Optional[Node], int]:
    explored: set = {initial}
    frontier: Stack = Stack()

    frontier.push(Node(initial, None))

    counter: int = 0
    while not frontier.empty:
        counter += 1

        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node, counter

        childs: list[MazeLocation] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node))

    return None, counter

def astar(successors: Callable, goal_test: Callable, initial: Node, heuristic: Callable) -> Optional[Node]:
    explored: set = {initial}
    frontier: PriorityQueue = PriorityQueue()

    frontier.push(Node(initial, None, 0, heuristic(initial)))

    while not frontier.empty:
        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node

        childs: list[MazeLocation] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node, current_node.cost + 1, heuristic(child)))

    return None

def count_astar(successors: Callable, goal_test: Callable, initial: Node, heuristic: Callable) -> Tuple[Optional[Node], int]:
    explored: set = {initial}
    frontier: PriorityQueue = PriorityQueue()

    frontier.push(Node(initial, None, 0, heuristic(initial)))

    counter: int = 0
    while not frontier.empty:
        counter += 1

        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node, counter

        childs: list[MazeLocation] = successors(current_node.state)

        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node, current_node.cost + 1, heuristic(child)))

    return None, counter

def node_to_path(node: Node) -> list[MazeLocation]:
    path: list[MazeLocation] = []
    while node.parent is not None:
        path.append(node.state)
        node = node.parent

    return path


if __name__ == "__main__":
    maze: Maze = Maze()
    node: Node = bfs(maze.successors, maze.goal_test, maze.start)
    if node is None:
        print("no path found, maze:\n" + str(maze))
    else:
        path: list[MazeLocation] = node_to_path(node)
        maze.mark(path)
        print("bfs: \n" + str(maze))
        maze.clear(path)

    node = dfs(maze.successors, maze.goal_test, maze.start)
    if node is None:
        print("no path found, maze:\n" + str(maze))
    else:
        path: list[MazeLocation] = node_to_path(node)
        maze.mark(path)
        print("dfs:\n" + str(maze))
        maze.clear(path)

    node = astar(maze.successors, maze.goal_test, maze.start, manhattan_distance(maze.goal))
    if node is None:
        print("no path found, maze:\n" + str(maze))
    else:
        path: list[MazeLocation] = node_to_path(node)
        maze.mark(path)
        print("astar:\n" + str(maze))
        maze.clear(path)

