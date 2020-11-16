"""
Take heed of this note from the readme:
 - The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 
This means I will need to take use of the Fractions class as I would lose information if I used floats.
"""
from fractions import Fraction, gcd

def transform_matrix(m):
    """
      Takes some transition matrix and changes its values from whole numbers to fractions in order to fit
      in the 32 bit integer limit

      Args:
        m: a transition matrix where the transient states use whole numbers and the absorbing states contain only 0
    """
    for row_index, row in enumerate(m):
        row_sum = sum(row)
        if row_sum == 0:
            # It is an absorbing state, set the probability it will return to itself as 1
            m[row_index][row_index] = 1
        else:
            # It is a transient state, find the probabilities of each state it will pass to
            for column_index, column in enumerate(row):
                m[row_index][column_index] = Fraction(column, row_sum)

def get_submatrix(m, rows, cols):
    """
      Gets the selected positions from the matrix and inserts them into the submatrix.

      Args:
        m: the larger matrix
        rows: list of the indexes of the rows to select from
        cols: list of the indexes of the columns to select from

      Returns:
        submatrix: the matrix filled with the selected values
    """
    submatrix = []
    for row in rows:
        new_row = []
        for col in cols:
            new_row.append(m[row][col])
        submatrix.append(new_row)
    return submatrix

def decompose_matrix(m, transient_states, absorbing_states):
    """
      Decomposes a transition matrix into its Q and R components as defined here: 
      https://brilliant.org/wiki/absorbing-markov-chains/

      Args:
        m: a transition matrix
        transient_states: the indexes of all the transient states in the transition matrix
        absorbing_states: the index of all the absorbing states in the transition matrix

      Returns:
        q: a matrix defining the probability of moving from one transient state to another
        r: a matrix defining the probability of moving from a transient state to an absorbing state.
    """
    # q is size len(transient_states)xlen(transient_states) and r is size len(transient_states)xlen(absorbing_states)
    return get_submatrix(m, transient_states, transient_states), get_submatrix(m, transient_states, absorbing_states)

def make_identity_matrix(size):
    """
      Makes the identity matrix for any size 

      Args:
        size: the size of the identity matrix to produce

      Returns:
        identity: the identity matrix of the specified size
    """
    identity = []
    # Create empty matrix
    for _ in range(size):
        identity.append([0] * size)
    # Fill in diagonal with 1
    for i in range(size):
        identity[i][i] = Fraction(1, 1)
    return identity

def subtract_matrices(a, b):
    """
      Subtracts matrix b from matrix a aka (a-b)

      Args:
        a: matrix to subtract from
        b: matrix to subtract away from a

      Returns:
        m: resulting matrix from a-b
    """
    m = []
    # Loop through each spot and subtract the values from eachother before adding to m.
    for row_index, row in enumerate(a):
        new_row = []
        for col_index, col in enumerate(b):
            new_row.append(a[row_index][col_index] - b[row_index][col_index])
        m.append(new_row)
    return m

def multiply_matrices(a, b):
    """
      Multiplies matrix a times matrix b

      Args:
        a: a matrix
        b: a matrix

      Returns:
        m: resulting matrix from a*b
    """
    m = []
    # Get lengths
    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])
    # Raise error if a_cols and b_rows are not equal because then you can't multiply a and b
    if not a_cols == b_rows:
        raise ArithmeticError('Can not multiply these matrices.')
    # New matrix will be a_rows * b_cols
    for row in range(a_rows):
        # Each row of a is multiplied by all columns of b
        new_row = []
        for col in range(b_cols):
            dot_product = Fraction(0, 1)
            for i in range(a_cols):
                # i represents position in the row of a and the column of b, moves one down each time
                dot_product += a[row][i]*b[i][col]
            new_row.append(dot_product)
        m.append(new_row)
    return m

def multiply_row_of_matrix(m, row_index, multiplier):
    """
      Scales a row of a matrix by a multiplier

      Args:
        m: matrix being scaled
        row_index: the index of the row being scaled
        multiplier: the multiplier to scale the row by

      Returns:
        Matrix with scaled row
    """
    # Multiplying a matrix by its identity gives you the matrix
    matrix_multiplier = make_identity_matrix(len(m))
    # Modify one part of the identity so that it scales the desired row
    matrix_multiplier[row_index][row_index] = multiplier
    # Multiply the modified identity and matrix together to get old matrix with scaled row
    return multiply_matrices(matrix_multiplier, m)

def add_multiple_of_row_to_matrix(m, source_row_index, multiplier, target_row_index):
    """
      Adds the source row times a multiplier to the target row

      Args:
        m: matrix being operated on
        source_row_index: the index of the row being scaled and added to the target row.
        multiplier: the multiplier to scale the source row by
        target_row_index: the row on which to add the scaled source row

      Returns:
        Matrix with the added row
    """
    # Multiplying a matrix by its identity gives you the matrix
    matrix_multiplier = make_identity_matrix(len(m))
    # Modify one part of the identity so that it scales the source row and adds it to the target row
    matrix_multiplier[target_row_index][source_row_index] = multiplier
    # Multiply the modified identity and matrix together to get old matrix with modified row
    return multiply_matrices(matrix_multiplier, m)

def invert_matrix(m):
    """
      Returns the inverse of matrix m

      Args:
        m: some matrix to find the inverse of

      Returns:
        inverse: the inverse of matrix m
    """
    size = len(m)
    inverse = make_identity_matrix(size)
    for col in range(size):
        # Portion used for scaling is always across the diagonal
        diagonal_row = col
        # Get multiplier
        multiplier = Fraction(1, m[diagonal_row][col])
        # Scale matrices
        m = multiply_row_of_matrix(m, diagonal_row, multiplier)
        inverse = multiply_row_of_matrix(inverse, diagonal_row, multiplier)
        # The source row is the diagonal row as that was the row just modified
        source_row = diagonal_row
        for target_row in range(size):
            # Don't let source row act on itself
            if source_row != target_row:
                multiplier = -m[target_row][col]
                m = add_multiple_of_row_to_matrix(m, source_row, multiplier, target_row)
                inverse = add_multiple_of_row_to_matrix(inverse, source_row, multiplier, target_row)
    return inverse

def lcm_of_integers(a, b):
    # Gets the least common multiple of 2 integers
    return (a * b) / gcd(a, b)

def lcm_of_denominators(denominators):
    # Gets the least common multiple of a list of integers
    lcm = 1
    for i in range(len(denominators)):
        lcm = lcm_of_integers(lcm, denominators[i])
    return lcm

def solution(m):
    # Initialize arrays
    absorbing_states = [] # List of the indexes of the rows containing a terminal state (all 0)
    transient_states = [] # List of the indexes of the rows not containing a terminal state
    # Find the indexes to populate the arrays
    for index, row in enumerate(m):
        if sum(row) == 0:
            absorbing_states.append(index)
        else:
            transient_states.append(index)
    # If only one absorbing state, return it with 100% probability
    if len(absorbing_states) == 1:
        return [1, 1]
    # Turn the matrix into a set of fractions to comply with the denominator restriction
    transform_matrix(m)
    # Decompose the matrix into Q and R defined here: https://brilliant.org/wiki/absorbing-markov-chains/
    q, r = decompose_matrix(m, transient_states, absorbing_states)
    # Get fundamental matrix N
    n = invert_matrix(subtract_matrices(make_identity_matrix(len(q)), q))
    # Get probability matrix M. First row will be state 0, so what I want.
    probability_matrix = multiply_matrices(n, r)
    probabilities = probability_matrix[0]
    # Find LCM of denominators 
    lcm = lcm_of_denominators([probability.denominator for probability in probabilities])
    # Scale all values by LCM so they become integers
    results = [probability.numerator * lcm / probability.denominator for probability in probabilities]
    # Add LCM as the denominator
    results.append(lcm)
    return results

print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))
# [7, 6, 8, 21]
print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
# [0, 3, 2, 9, 14]