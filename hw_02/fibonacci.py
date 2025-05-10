def f1(n):
    if n == 1 or n == 2:
        return 1
    return f1(n-1) + f1(n-2)

def f2(n):
    if n == 1:
        return 1
    if n == 2:
        return 1

    a = 1
    b = 1

    for i in range(n-2):
        a, b = b, a+b

    return b



