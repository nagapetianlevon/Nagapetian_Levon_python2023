# через список (в роли стека)
def correct_br_sq_1(seq):
    s = []
    for i in seq:
        if i == '(':
            s.append(i)
        else:
            if s:
                s.pop()
            else:
                return False
    return (not s)

# без списка (стека)
def correct_br_sq_2(seq):
    c = 0 #счетчик
    for i in seq:
        if i == '(':
            c+=1
        else:
            if c:
                c-=1
            else:
                return False
    return (not c)



