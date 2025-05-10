def plus_one(l):
    num = 0

    for i in l:
        num*= 10
        num+=i

    num+=1

    d = []

    while(num):
        c = num%10
        d.append(c)
        num//=10

    return d[::-1]



l = [8, 9, 9, 9]

print(plus_one(l))