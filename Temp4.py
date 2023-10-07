import math


def myPow(x: float, n: int) -> float:
    # The most basic idea anyone can implement
    if n == 0:
        return 1

    if n < 0:
        n, x = abs(n), 1 / x
    result = x

    value = helper(x, n)
    result = 1
    for i in value:
        if i != 0:
            result *= i

    return result


def helper(x, n):
    if n == 1:
        return [x]

    result = []
    odds = [x if n % 2 == 1 else 1]

    for i in range(n // 2):
        result.append(x * x)
    if len(result) % 2 == 1:
        odds.append(result.pop())
    if len(result) != 0:
        result = helper(result[0], len(result))

    return result + odds










print(myPow(0.0001, 2147483647))
print(myPow(2, 10))
print(myPow(2, -2))

