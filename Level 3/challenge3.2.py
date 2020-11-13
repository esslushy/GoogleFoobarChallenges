def solution(maze):
    # Starting and ending Node positions
    starting_position = (0, 0)
    ending_position = (len(maze)-1, len(maze[0])-1) # Uses y then x because that is how matrix is set up. (row, columns)
    # Run search algorithm. 
    return search(maze, starting_position, ending_position)

class Node:
    """
      Node for BFS Algorithm

      Args:
        x: What column the node is in
        y: What row the node is in
        maze: The maze the node occupies. Maze is in form (row, column) or (y, x)
        can_remove_wall: If the node can remove a wall or not.
    """
    def __init__(self, x, y, maze, can_remove_wall=True):
        self.x = x
        self.y = y
        self.maze = maze
        self.num_rows = len(maze)
        self.num_columns = len(maze[0])
        self.can_remove_wall = can_remove_wall

    def __hash__(self):
        # For dictionary
        return self.x ^ self.y

    def __eq__(self, other):
        # Equal if same position and both can remove a wall
        return self.x == other.x and self.y == other.y and self.can_remove_wall == other.can_remove_wall

    def get_neighbors(self):
        """
          Gets all neighbors of current Node
        """
        # Initialize list to hold neighbor nodes
        neighbors = []
        # Make list of all possible moves
        possible_moves = [
            [-1, 0], # Move left
            [0, -1], # Move up
            [1, 0], # Move right
            [0, 1] # Move down
        ]
        # Loop through all possible moves
        for move in possible_moves:
            # Create new neighbor
            neighbor = Node(self.x + move[0], self.y + move[1], self.maze)
            # Ensure the position is within maze boundaries
            if neighbor.x < 0 or neighbor.y < 0 or neighbor.x >= self.num_columns or neighbor.y >= self.num_rows:
                # If it isn't skip adding this neighbor
                continue
            # Check for wall a wall blocking the neighbor. If there is, see if the you can remove it.
            if self.maze[neighbor.y][neighbor.x] != 0:
                if self.can_remove_wall:
                    neighbor.can_remove_wall = False
                else:
                    # Don't add this neighbor as it can't exist
                    continue
            else:
                # If the area is passable, neighbor inherits wall breaking ability from parent
                neighbor.can_remove_wall = self.can_remove_wall
            # Add to neighbor list
            neighbors.append(neighbor)
        return neighbors

def search(maze, start, end):
    """
      BFS function

      Args:
        maze: the maze to find the path through
        start: starting coordinates in form (row, column) (y, x)
        end: the coordinates to end at in form (row, column) (y, x)
    """
    source_node = Node(start[1], start[0], maze)
    queue = [source_node] # Start with source node.
    distance_map = { source_node : 1 } # How many steps it took to reach a node
    # Loop through all nodes in queue until you run out or find the ending node
    while len(queue) > 0:
        # Grab current node out of the queue
        current_node = queue.pop(0)
        # Check to see if it is the ending node
        if current_node.x == end[1] and current_node.y == end[0]:
            return distance_map[current_node]
        # If not, get neighbors and add neighbors to distance map and queue if they aren't already on there.
        for neighbor in current_node.get_neighbors():
            if neighbor not in distance_map:
                distance_map[neighbor] = distance_map[current_node] + 1
                queue.append(neighbor)

print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])) # 7
print(solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])) # 11