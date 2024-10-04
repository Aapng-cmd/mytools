from collections import deque

def bfs(labyrinth, start):
    """
    Performs a BFS to find a path from the start point to (0, 0) in the labyrinth.

    Args:
        labyrinth: 2D list of lists, where each element is a list of 4 booleans
            representing the walls in the up, right, down, and left directions.
        start: tuple of two integers, representing the starting point.

    Returns:
        A list of tuples, representing the path from the start point to (0, 0).
        If no path is found, returns an empty list.
    """
    queue = deque([(start, [start])])  # Initialize the queue with the start point
    visited = set([start])  # Keep track of visited points

    while queue:
        point, path = queue.popleft()
        if point == (0, 0):
            return path  # Found the goal, return the path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, right, down, left
            x, y = point[0] + dx, point[1] + dy
            if (0 <= x < len(labyrinth)) and (0 <= y < len(labyrinth[0])):  # Check bounds
                if dx == -1:  # up
                    wall_index = 0
                elif dx == 1:  # down
                    wall_index = 2
                elif dy == -1:  # left
                    wall_index = 1
                elif dy == 1:  # right
                    wall_index = 3
                if not labyrinth[y][x][wall_index]:  # Check wall in the direction
                    if (x, y) not in visited:
                        queue.append(((x, y), path + [(x, y)]))
                        visited.add((x, y))
    print(visited)
    return []  # No path found

# Example usage:
labyrinth = []
start = (0, 0)
print(labyrinth[2][0])
path = bfs(labyrinth, start)
print(path)  # Output: [(3, 2), (2, 2), (2, 1), (1, 1), (1, 0), (0, 0)]
