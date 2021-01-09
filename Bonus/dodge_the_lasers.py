from math import floor, sqrt
# Beatty's sequence with sqrt(2)

# General form would be for n wanted instances
# sum of floor(sqrt(2)*k) for k to n
# Even more general
# S(a, n) where a is the irrational and n is the amount of inputs
# S(a,n) = summation k=1 to n floor(a*k)

# https://mathworld.wolfram.com/BeattySequence.html
# https://math.stackexchange.com/questions/2052179/how-to-find-sum-i-1n-left-lfloor-i-sqrt2-right-rfloor-a001951-a-beatty-s
# 1<sqrt(2)<2 so the formula a^-1 + b^-1 = 1 applies
# floor(an) and floor(bn) partition all counting numbers
# To sum all counting numbers up to n
# let m = floor(a*n)
# S(a, n) + S(b, floor(m/b)) = sum of k=1 to n = m(m+1)/2
# S(a, n) = m(m+1)/2 - s(b, floor(m/b))

# Have to use this so it is not cut off by rounding in computer. Equal to sqrt(2)-1 * 10**100
minus_sqrt2 = 4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727

# Has to handle up to 10^100 as an input, so brute force won't work
def solution(s):
    return str(solver(s))

def solver(s):
    # Number of iterations
    n = int(s)
    # If 0 iterations just return 0
    if n == 0:
        return 0
    # If 1 iteration just return 1
    if n == 1:
        return 1
    # N prime
    n_prime = (minus_sqrt2 * n) // 10**100
    # Sum
    sum_of_beatty = n*n_prime + n*(n+1)/2 - n_prime*(n_prime+1)/2
    sum_of_beatty -= solver(n_prime)
    return int(sum_of_beatty)

print(solution('5'))# 19
print(solution('77'))# 4208
print(solution(str(10**100)))