# from lxml import etree


# with open('xml.txt', 'w') as f:
#     for event, element in etree.iterparse('adsc/adsc.fcd.xml', events=('end', ), tag='timestep'):
#         f.write(str(element.attrib) + '\n')

#         for info in element.iter():
#             if info.tag in ('vehicle'):
#                 f.write(str(info.attrib) + '\n')

#         f.write('-----------\n')
#         # element.close()
#         element.clear()


from functools import wraps

def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

@memo
def fibm(n):
    if n < 2:
        return 1
    return fibm(n-1) + fibm(n-2)


# def fib(n):
#     if n == 1 or n == 0:
#         return 1
#     return fib(n-1) + fib(n-2)


import sys
sys.setrecursionlimit(1000000000)



def memoize(f):
    cache = {}
    return lambda *args: cache[args] if args in cache else cache.update({args: f(*args)}) or cache[args]

@memoize
def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)

print fib(1000)
