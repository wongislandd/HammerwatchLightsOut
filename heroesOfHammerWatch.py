from copy import deepcopy
from collections import deque
from itertools import chain

class StepNode:
    def __init__(self, parent, step, grid):
        self.parent = parent
        self.step = step
        self.grid = grid


def take_step(grid, step):
    newGrid = deepcopy(grid)

    x, y = step

    # current
    newGrid[y][x] = 1 - newGrid[y][x]

    # down
    if y + 1 < len(newGrid):
        newGrid[y + 1][x] = 1 - newGrid[y + 1][x]

    # up
    if y - 1 >= 0:
        newGrid[y - 1][x] = 1 - newGrid[y - 1][x]

    # left
    if x - 1 >= 0:
        newGrid[y][x - 1] = 1 - newGrid[y][x - 1]

    # right
    if x + 1 < len(newGrid):
        newGrid[y][x + 1] = 1 - newGrid[y][x + 1]

    return newGrid


def is_solved(grid):
    return sum(sum(x) for x in grid) == len(grid) * len(grid)


def get_possible_steps(grid):
    steps = [(a, b) for a in range(len(grid)) for b in range(len(grid))]
    steps.reverse()
    return steps


def bfs_tree_solver(grid):
    possibleSteps = get_possible_steps(grid)
    queue = deque()
    visited = set()

    for steps in possibleSteps:
        # Initialize queue with all initial moves and resulting grid
        newGrid = take_step(grid, steps)
        queue.append(StepNode(None, steps, newGrid))

    while queue:
        currentNode = queue.popleft()

        # Never go further down a path we've already seen
        if bit_string(currentNode.grid) in visited:
            continue
        else:
            visited.add(bit_string(currentNode.grid))

        # Check if this current grid is solved
        if is_solved(currentNode.grid):
            return currentNode

        for steps in possibleSteps:
            if steps != currentNode.step:
                newGrid = take_step(currentNode.grid, steps)
                queue.append(StepNode(currentNode, steps, newGrid))

    # There should always be a solution
    return -1


def bit_string(grid):
    return ''.join([str(x) for x in list(chain.from_iterable(grid))])


def solve(grid):
    leafNode = bfs_tree_solver(grid)
    if leafNode != -1:
        shortestPath = trace_node_parents(leafNode)
        run_path(grid, shortestPath)


def run_path(grid, path):
    print(f"Shortest path is...{path}")
    print("Original grid")
    print_grid(grid)
    currentGrid = grid
    for step in path:
        print("-" * 20)
        print(f"Take step {step}")
        currentGrid = take_step(currentGrid, step)
        print_grid_with_highlight(currentGrid, step)


def print_grid_with_highlight(grid, step):
    highlightX, highlightY = step
    for x in range(len(grid)):
        rowStr = ""
        for y in range(len(grid[x])):
            entry = grid[x][y]
            if x == highlightX and highlightY == y:
                rowStr += f"[{entry}]"
            else:
                rowStr += f" {entry} "
        print(f"| {rowStr} |")


def print_grid(grid):
    print_grid_with_highlight(grid, (-1, -1))


def trace_node_parents(node):
    trace = []

    currentNode = node

    # Track the parents all the way up
    while currentNode.parent:
        trace.append(currentNode.step)
        currentNode = currentNode.parent

    # Append the root of this path
    trace.append(currentNode.step)

    # Since we went from leaf -> root, we want the readout as root -> leaf
    trace.reverse()

    return trace


if __name__ == '__main__':
    sampleGrid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1]
    ]
    solve(sampleGrid)
