# Flowrate challenge - Find the Maximum flow through a graph
# Ford-Fulkerson with BFS
# Make sure to transform graph so one source and one sink
# https://brilliant.org/wiki/ford-fulkerson-algorithm/

# At most 2000000 bunnies can be transferred at a time

def solution(entrances, exits, path):
    # Check for multiple sources
    if len(entrances) > 1:
        # Pad path to account for new source. Since it is a source nothing will go to it
        pad_array(path, 0)
        # Create the source with max flow (2000000) to the original sources
        source = [0] * len(path[0])
        for connection in entrances:
            source[connection] = 2000000
        # Add source to path
        path.append(source)
        # Set that source to the entrance
        entrances = [len(path) - 1]
    # Check for multiple sinks
    if len(exits) > 1:
        # Pad path to account for new sink.
        pad_array(path, 0)
        # Create new sink
        sink = [0] * len(path[0])
        path.append(sink)
        # Attach old sinks to new sink with maximum flow availability
        for connection in exits:
            path[connection][len(path[0]) - 1] = 2000000
        # Set the new sink to the exit
        exits = [len(path) - 1]
    # Pull Entrances and exits out of the array
    entrances = entrances[0]
    exits = exits[0]
    # Use Ford-Fulkerson to find maximum flow
    return ford_fulkerson(path, entrances, exits)

def pad_array(matrix, value):
    """
      Pads the left side of the rows of a matrix with the given value

      Args:  
        matrix: matrix to be padded  
        value: the value to use to pad the array  
    """
    for row in matrix:
        row.append(value)
    return matrix


def BFS(graph, s, t, parent):
    """
      Populates parent with nodes to visit and returns true if there are nodes left to visit

      Args:
        graph: an array of arrays of integers where graph[a][b] = c is the max flow, c, between a and b.
        s: Source of the graph
        t: Sink or "end" of the graph
        parent: Array holding the nodes to visit
    """
    # Start with none of the nodes visited
    visited = [False] * len(graph)
    # Begin queue at source. Will hold all nodes yet to visit
    queue = []
    queue.append(s)
    # "Visited" aka will visit source node
    visited[s] = True
    # While there are still nodes in queue
    while queue:
        # Current searching node
        u = queue.pop(0)
        # Check each possible connection
        for ind in range(len(graph[u])):
            # If that connection hasn't been visited and is recieving source
            if visited[ind] is False and graph[u][ind] > 0:
                # Add the connection to the queue of ones to search
                queue.append(ind)
                # Set it to being visited
                visited[ind] = True
                # Add the search to the parent
                parent[ind] = u

    return True if visited[t] else False


def ford_fulkerson(graph, source, sink):
    """
      Uses the Ford-Fulkerson algorithm to find the maximum flow in a graph between
      one source and one sink.

      Args:
        graph: an array of arrays of integers where graph[a][b] = c is the max flow, c, between a and b.
        source: Source of the flow graph
        sink: Sink of the flow graph
    """
    # This array is filled by BFS and used to store path. 
    parent = [-1] * (len(graph))
    # Initialize maximum flow
    max_flow = 0
    # Continue to look through graph while there are unexplored nodes. Also populate parent of nodes to search
    while BFS(graph, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        # Continue moving through graph under source and sink are the same
        while s != source:
            # Get minimum value in each step as it is resisted by the one before
            path_flow = min(path_flow, graph[parent[s]][s])
            # Go to next node
            s = parent[s]

        max_flow += path_flow
        v = sink
        # Modify each connection by residual flow
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    return max_flow

print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))
# Output: 6
print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
# Output: 16