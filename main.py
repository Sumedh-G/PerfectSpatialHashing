import sympy
import numpy as np

def generateHashTable(points):
    n = len(points)
    print(f"{n=}")
    m = int(sympy.nextprime(np.sqrt(n)))  #type:ignore
    print(f"{m=}")
    increment_factor = 2
    r = int(np.sqrt(n) / (increment_factor))

    h0 = np.array(points % m, dtype="int64")
    h1 = np.array(points % r, dtype="int64")
    print(f"Starting with {h1=}")
    print(np.column_stack((h0, h1)))

    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"Stating with {phashes=}")
    while len(phashes) != n:
        print(f"Trying {r=}")
        r *= increment_factor
        h1 = np.array(points % r, dtype="int64")
        phashes = np.unique(np.column_stack((h0, h1)), axis=0)

    h1 = np.array(points % r, dtype="int64")
    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"{r=}")
    print(f"{h0=}")
    print(f"{h1=}")

    print(f"{phashes=}")
    groups = [[p for p in phashes if np.all(p[2:] == k)] for k in np.unique(h1, axis=0)][::-1]
    print(f"{groups=}")

    phi = np.zeros((r, r, 2), dtype="int64")
    h = np.zeros((m, m, 2), dtype="int64") - 1

    getHash = lambda k : (k[:2] + phi[k[3]][k[2]]) % m
    i = 0
    oc = 0
    while i < len(groups):
        valid = True
        for g in groups[i]:
            gh = getHash(g)
            print(f"{gh=}")
            if np.all(h[gh[1]][gh[0]] != np.array([-1, -1])):
                valid = False

        if valid:
            for g in groups[i]:
                gh = getHash(g)
                h[gh[1]][gh[0]] = g[:2]
            print(f"{h=}")
            i += 1
            oc = 0
        else:
            offseti = groups[i][0][2:]
            print(f"{offseti=}")
            oc += 1
            print(f"{oc=}")
            assert oc < m**2, "oc exploded"
            phi[offseti[1]][offseti[0]] = np.array([oc % m, oc // m])
            print(f"{phi=}")


if __name__ == "__main__":
    generateHashTable(
        np.array([[1, 2], [4, 5], [13, 45], [11, 17], [15, 45]])
    )
