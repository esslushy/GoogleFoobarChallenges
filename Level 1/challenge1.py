def solution(s):
    # Your code here
    # Slice string into single letters, then 2, then 3
    for i in range(1, len(s)+1):
        cake = s
        segments = []
        while len(cake) > 0:
            segments.append(cake[:i])
            cake = cake[i:]
        # Check to see if they are all the same, if they are return the length, if not keep trying
        all_equal = True
        for segment in segments:
            if not segments[0] == segment:
                all_equal = False
                break

        if all_equal:
            return len(segments)

print(solution('abccbaabccba'))