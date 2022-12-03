# def rand_generator(seed, N=10**6, a=0, b=10, integer=True):
#     rands = []
#     if integer:
#         for i in range(N):
#             num = int(
#                 a+(b-a)*(abs(hash(str(hash(str(seed)+str(i+1))))) % 10**13)/10**13)
#             rands.append(num)
#         return rands
#     else:
#         for i in range(N):
#             num = a+(b-a)*(abs(hash(str(hash(str(seed)+str(i+1))))) %
#                            10**13)/10**13
#             rands.append(num)
#         return rands


def rand_generator(a: int, b: int, integer=True):
    seed = b//a
    const = 10**13
    num = 0
    num = int(a+(seed)*(abs(hash(str(seed))) % const)/const)
    return int(num) if integer else num


from random import randint 
n = int(input('Введите число: '))
list_n = [28, -46, 14, -14, -5, -3, -2]
print(list_n)
print('=>')
i=0 
while i < len(list_n):
    if list_n[i] < 0:
        list_n.insert(i+1, 0)
        i+=1
    else:
        i+=1
print(list_n)
