# Celular automata question
# Have to find preimage to a celular automata with set rule

# All possible precursors
precursors = {
    0: (
        ((0, 0), (0, 0)),
        ((1, 1), (0, 0)),
        ((1, 0), (1, 0)),
        ((1, 0), (0, 1)),
        ((0, 1), (1, 0)),
        ((0, 1), (0, 1)),
        ((0, 0), (1, 1)),
        ((1, 1), (1, 0)),
        ((1, 1), (0, 1)),
        ((1, 0), (1, 1)),
        ((0, 1), (1, 1)),
        ((1, 1), (1, 1))
    ),
    1: (
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
        ((0, 1), (0, 0)),
        ((1, 0), (0, 0))
    )
}

def solution(graph):
    """
      This function counts all possible previous states that could lead to the current state
      of the nebula given by graph.

      The states evolve following these rules:
       - Each 2x2 area determines the 1x1 area of the next section, so it shrinks by 1 each time (4x4 --> 3x3)
       - If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, 
         then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

      So When finding the previous, it will be one larger than the current.

      This counts precolumns by generating them all and counting the ones that can be connected start to finish
      by intermediary columns so no impossible precursors are counted and only whole images are found.

      Args:
        graph: current state of nebula
    """
    # Turn graph from bools into ints. 1 = cell has gas; 0 = cell does not have gas. Makes future calculations easier.
    graph = [[int(cell) for cell in row] for row in graph]
    # Group into columns rather than rows. So first index is x coord, second is y
    graph_columns = tuple(zip(*graph))
    # Get intial precolumns
    initial_precolumns = generate_precolumn(graph_columns[0])
    # Setup initial dictionary holding counts of all possible connections
    preimage_counter = {}
    for column_pair in initial_precolumns:
        # Each iniial left side column (has no precursors) has 1 connected to it at the start
        preimage_counter[column_pair[0]] = 1
    # Cycle through graph and begin counting preimages of ones that fit together properly
    for column in graph_columns:
        precolumns = generate_precolumn(column)
        # Dictionary for counting next set of preimages
        new_preimage_counter = {}
        for column_pair in precolumns:
            if column_pair[0] not in preimage_counter:
                # This column has no previous connections to it, so it can't have any forward connections. Adds no value.
                preimage_counter[column_pair[0]] = 0
            if column_pair[1] not in new_preimage_counter:
                # If the column pair is not yet in the new count, initialize it
                new_preimage_counter[column_pair[1]] = 0
            # Add all possible previous connections to this new connection
            new_preimage_counter[column_pair[1]] += preimage_counter[column_pair[0]]
        # Shift the counter down, so the previous endpoints are now the midpoints to connect to the next column pair
        preimage_counter = new_preimage_counter
    # Sum of all possible endings
    return sum(preimage_counter.values())

def generate_precolumn(column):
    """
      Generates all possible binary number pairs of columsn that could come before it.

      Args:
        column: the column to generate the previous possibilities of.
    """
    # List of all possible additions each section can add to the column
    possible_additions = ((0, 0), (0, 1), (1, 0), (1, 1))
    # Generate intial precolumn seed from first item in column
    current_precolumns = precursors[column[0]]
    # Iterate through the rest of the column. Starts at one
    for i in range(1, len(column)):
        new_precolumns = []
        # Loop through all precolumns
        for precolumn in current_precolumns:
            # Test each addition to see if it would evolve to the right state
            for addition in possible_additions:
                if evolve([precolumn[i], addition]) == column[i]:
                    # If evolves properly, save it to the array
                    new_precolumns.append(precolumn+(addition,))
        # Change current columns to the newly made set of possible columns and continue on down the column.
        current_precolumns = tuple(new_precolumns)
    # Make sure the list of possible precolumns are in the form of columns
    current_precolumns = [tuple(zip(*precolumn)) for precolumn in current_precolumns]
    # Return the new columns as numbers based on the binary form of the list
    return [tuple(list_to_number(col) for col in precolumn) for precolumn in current_precolumns]

def list_to_number(column):
    """
      Turns a columns of 0s and 1s to an integer

      Args:
        column: List of 0s and 1s to turn into a number
    """
    # Cast column integers to strings
    column = [str(cell) for cell in column]
    # Turn to an integer with base2
    return int(''.join(column), 2)

def evolve(block):
    """
      Evolves the passed block given by the rules

      Args:
        block: a 2x2 matrix to be evolved
    """
    # Get sum of block
    value = sum(block[0]) + sum(block[1])
    if value == 1:
        # Return that it is a gas if there is only 1 cell with gas in it
        return 1
    else:
        # If there is not only 1 cell with gas in it, return that there is no gas
        return 0

print(solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]))
# Expected: 11567
print(solution([[True, False, True], [False, True, False], [True, False, True]]))
# Expected: 4
print(solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]))
# Expected: 254