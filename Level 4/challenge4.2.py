from copy import deepcopy

def solution(times, times_limit):
    # Special case if there are no intermediary bunnies to pick up.
    # Reminder times[0] is the start and times[-1] is the end so if it is 2 or less you just go from start to exit
    if len(times) <= 2:
        return []
    # Apply Floyd-Warshall Algorithm.
    new_times = floyd_warshall(times)
    # Check for negative cycles
    if negative_cycles(new_times):
        # If a negative cycle exists, all bunnies can be picked up, so return a list of all prisoner ids
        # Prisoner ids start from 0 and there are 2 less than the full set of times (no start or bulkhead)
        return list(range(len(times)-2))
    # If no negative cycles, do dfs
    return new_times

def floyd_warshall(graph):
    """
      Calculates the shortest distance between any 2 vertices in the graph

      Args:
        graph: the graph to run the algorithm over
    """
    # Create a deep copy to run manipulations on
    new_graph = deepcopy(graph)
    # Rotate through graph
    for intermediary in range(len(new_graph)):
        for start in range(len(new_graph)):
            for end in range(len(new_graph)):
                # Figure out if it is better to reach node at end through the intermediary or just straigh tthrough
                newDistance = new_graph[start][intermediary] + new_graph[intermediary][end]
                if newDistance < new_graph[start][end]:
                    # If it is, set (start, end) to that new shortest distance
                    new_graph[start][end] = newDistance
    return new_graph

def negative_cycles(graph):
    """
      Returns true if there are any negative cycles in the graph

      Args:
        graph: the graph to check for negative cycles
    """
    for i in range(len(graph)):
        # If the path from something to itself is less than 0, then there is a negative cycle
        if graph[i][i] < 0:
            return True
    return False

print(solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1))
# Expected: [1, 2]
print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3))
# Expected: [0, 1]