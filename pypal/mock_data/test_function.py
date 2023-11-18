def badFibonacci(n):
    "cdlkmf"
    a, b = 0, 1
    if n == 0:
        return a
    for i in range(1, n):
        a, b = b, a + b
    return b
