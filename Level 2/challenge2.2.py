from functools import reduce

def solution(xs):
    # If it is only one number return that value
    if len(xs) == 1:
        return str(xs[0])
    # Get out positive and negative numbers. Ignore zeroes
    pos_nums = []
    neg_nums = []
    for num in xs:
        if num > 0:
            pos_nums.append(num)
        elif num < 0:
            neg_nums.append(num)
    # If negative array has an odd length, remove the smallest negative
    if len(neg_nums) % 2 == 1:
        neg_nums.remove(max(neg_nums)) # Uses max because smallest refers only to magnitude and -1 > -2 in terms of magnitude.
    # Multiply together positive array. 
    if len(pos_nums) > 0:
        mult_pos_nums = reduce(lambda x, y: x*y, pos_nums)
    else:
        mult_pos_nums = 1
    # Multiply together negative array
    if len(neg_nums) > 0:
        mult_neg_nums = reduce(lambda x, y: x*y, neg_nums)
    else:
        mult_neg_nums = 1
    # Check if all 0
    if len(neg_nums) == 0 and len(pos_nums) == 0:
        return "0"
    return str(mult_pos_nums * mult_neg_nums)
    

print(solution([2, 0, 2, 2, 0]))
print(solution([-2, -3, 4, -5]))
print(solution([0, -0, 0]))
print(solution([-1]))

