import sympy
import numpy as np

def generateHashTable(points):
    n = len(points)
    m = int(sympy.nextprime(np.sqrt(n)))  #type:ignore

    h0 = np.array(points % m, dtype="int64")
    increment_factor = 2
    r = int(np.sqrt(n) / (increment_factor))

    h = np.zeros(shape=(m, m, 2), dtype="int64") - 1
    h1 = np.array(points % r, dtype="int64")
    phi = np.zeros(shape=(r, r, 2), dtype="int64")


    print(f"{points=}\n{n=}\n{m=}\n{r=}\n{h0=}\n{h1=}\n{priorityList=}\n{offsets=}\n{combined_map=}\n{h=}")


if __name__ == "__main__":
    generateHashTable(
        np.array([[2, 3], [5, 18], [13, 41], [13,42], [14, 42], [13, 43]])
    )
