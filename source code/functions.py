import numpy as np


# needs specific array of values for x-es
def rastrigin(x):
    x = np.asarray(x)
    n = len(x)
    return 10 * n + sum(x ** 2 - 10 * np.cos(2 * 3.14 * x))


# needs specific array of values for x-es
def michalewicz(x):
    x = np.asarray(x)
    m = 10.
    n = len(x)
    j = np.arange(1., n + 1)
    return -sum(np.sin(x) * np.sin(j * x ** 2 / 3.14) ** (2 * m))


def dejong(x):
    x = np.asarray(x)
    return sum(x**2)


def schwefel(x):
    x = np.asarray(x)
    # global minimum..whatever
    # f(x)=-n·418.9829; x(i)=420.9687, i=1:n.
    return sum(-x * np.sin(np.sqrt(np.abs(x))))

