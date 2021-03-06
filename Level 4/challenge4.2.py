from copy import deepcopy
from itertools import combinations, permutations

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
    # If no negative cycles, do dfs to find the most bunnies one can pick up.
    return get_most_bunnies(new_times, times_limit)

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

def create_subsets(main_set):
    """
      Creates all possible subsets of the main set

      Args:
        main_set: the set to create subsets of
    """
    # Initialize subsets
    subsets = []
    # Use itertools to create all combinations of each possible length
    for n in range(1, len(main_set)+1):
        subsets.extend(combinations(main_set, n))
    return subsets

def get_most_bunnies(graph, time_limit):
    """
      Uses DFS to check each possible collection of bunnies to see which one is the most optimal.

      Args:
        graph: the graph that can be checked over.
    """
    # Initialize list of bunnies. -2 to skip entrance and exit
    bunny_ids = list(range(len(graph)-2))
    # Create all subsets to try
    bunny_sets = create_subsets(bunny_ids) # Using tuples, but should be fine as long as it returns a list at the end
    # Sort the subsets so they are in order of lowest prisoner id to highest
    bunny_sets = sorted(bunny_sets)
    # Initial optimal_bunny_set variable
    optimal_bunny_set = ()
    # Test each subset
    for subset in bunny_sets:
        # Test each permutation of the subset. AKA any order of picking up the bunnies
        for permutation in permutations(subset):
            # Initialize variable to track and accumulate distance
            distance = 0
            previous_bunny = 0 # 0 is the start with no bunny
            # Iter through picking up each bunny
            for bunny_id in permutation:
                # Set up next_bunny to move to. 1 is added because bunny ids are 1 behind there actual location in graph
                next_bunny = bunny_id + 1
                # Add distance from previous bunny to next
                distance += graph[previous_bunny][next_bunny] 
                # Set previous bunny to the bunny just moved to
                previous_bunny = next_bunny
            # Add last iteration from final bunny to end
            distance += graph[previous_bunny][len(graph)-1]
            # Make sure distance passes checks
            if distance <= time_limit and len(subset) > len(optimal_bunny_set):
                # If it does, make the current subset the next optimal subset
                optimal_bunny_set = subset
    # Cast optimal_bunny_set to list so it can pass checks
    return list(optimal_bunny_set)

print(solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1))
# Expected: [1, 2]
print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3))
# Expected: [0, 1]