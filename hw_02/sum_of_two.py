def two_sum(l, n):
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[i] + l[j] == n:
                return [i, j]

print(two_sum([2, 7, 11, 15], 9))
print(two_sum([4, 5, 9, 5], 10))
print(two_sum([-4, 3, 10, 0], -1))
