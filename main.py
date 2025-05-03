import sympy
import numpy as np

def generateHashTable(points):
    n = len(points)
    print(f"{n=}")
    m = int(sympy.nextprime(np.sqrt(n)))  #type:ignore
    print(f"{m=}")

    h0 = np.array(points % m, dtype="int64")
    increment_factor = 2
    r = int(np.sqrt(n) / (increment_factor))

    while True:
        h1 = np.array(points % r, dtype="int64")
        if len(np.unique(np.array([h0.T, h1.T]).T, axis=0)) != len(np.array([h0.T, h1.T]).T):
            r *= increment_factor
        else:
            break
    print(f"{r=}")
    phashes = np.unique(np.array([h1.T, h0.T]).T, axis=0)

    groups = {}
    for h, p in phashes:
        if tuple(h) in groups:
            groups[tuple(h)].append(p)
        else:
            groups[tuple(h)] = [p]
    points = sorted([[np.array(x), np.array(k)] for k, x in groups.items()], key=lambda x:len(x[0]), reverse=True)

    h = np.zeros(shape=(m, m, 2), dtype="int64") - 1
    phi = np.zeros(shape=(r, r, 2), dtype="int64")
    accomodated = False
    while not accomodated:
        for group in points:
            for index in group[0] + phi[group[1][1]][group[1][0]]:
                print(index)
        break


if __name__ == "__main__":
    generateHashTable(
        np.random.randint(0, 101, size=(50, 2))
    )
