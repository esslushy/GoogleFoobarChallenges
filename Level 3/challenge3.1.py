from functools import reduce

# XOR follows a 4 long pattern when in a chain based on the first value (x) in the chain and the last value (y) in a chain
# x = start
# y = x+length-1 b/c it takes length -1 jumps to get to end of chain
# pattern if x is:
# Even: [y, 1, y+1, 0]
# Odd: [x, x^y, x-1, (x-1)^y]

def fast_xor(start, end):
    # Run the fast XOR based on the pattern
    if start % 2 == 0: # AKA is even
        xor_options = [end, 1, end+1, 0]
    else: # AKA is odd
        xor_options = [start, start^end, start-1, (start-1)^end]
    # Find spot in pattern. Essentially what part of the pattern of 4 it ends on
    spot = (end-start) % 4
    return xor_options[spot]

def solution(start, length):
    # Answer placeholder. Use 0 because it doesn't effect XOR
    checksum = 0
    # Cycle through length to get all the rows
    for i in range(length):
        # Beginning of each line is start + how many rows down it is
        beginning = start + (length * i)
        # End is length - i - 1 jumps away. i represents how the line shortens by 1 each time
        end = beginning + (length - 1) - i
        # Run beginning and end through the pattern checker to more efficiently xor
        checksum ^= fast_xor(beginning, end)
    # Return checksum
    return checksum

print(solution(0, 3))
print(solution(17, 4))