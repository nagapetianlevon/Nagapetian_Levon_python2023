def unique(str):

    d = dict()

    for char in str:
        if char not in d:
            d[char] = 0
        d[char]+=1

    return d

print(unique(("aaabbcba")))