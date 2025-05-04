import sympy
import numpy as np
import matplotlib.pyplot as plt

def generateHashTable(points):
    n = len(points)
    print(f"{n=}")
    m = int(sympy.nextprime(np.sqrt(n)))  #type:ignore
    print(f"{m=}")
    increment_factor = 1.2
    r = int(np.sqrt(n) / 2)
    print(f"Initial {r=}")

    h0 = np.array(points % m, dtype="int64")
    h1 = np.array(points % r, dtype="int64")
    print(f"Starting with {h1=}")
    print(np.column_stack((h0, h1)))

    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"Stating with {phashes=}")
    while len(phashes) != n:
        print(f"Trying {r=}", end="\r", flush=True)
        r = int(r * increment_factor)
        h1 = np.array(points % r, dtype="int64")
        phashes = np.unique(np.column_stack((h0, h1)), axis=0)

    h1 = np.array(points % r, dtype="int64")
    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"Settled on {r=}")
    print(f"{h0=}")
    print(f"{h1=}")

    print(f"{phashes=}")
    groups = [phashes[np.all(phashes[:, 2:] == k, axis=1)] for k in np.unique(h1, axis=0)][::-1]
    print("Created groups")

    phi = np.zeros((r, r, 2), dtype="int64")
    h = np.zeros((m, m, 2), dtype="int64") - 1

    getHash = lambda k : (k[:2] + phi[k[3]][k[2]]) % m
    i = 0
    oc = 0
    while i < len(groups):
        valid = True
        for g in groups[i]:
            gh = getHash(g)
            if np.all(h[gh[1]][gh[0]] != np.array([-1, -1])):
                valid = False

        if valid:
            for g in groups[i]:
                gh = getHash(g)
                h[gh[1]][gh[0]] = g[:2]
            i += 1
            oc = 0
            random_start = np.random.randint(0, r-1)
            print("OffsetFound")
        else:
            offseti = groups[i][0][2:]
            oc += 1
            print(f"{oc=}", end="\r", flush=True)
            assert oc < m**2, "oc exploded"
            phi[offseti[1]][offseti[0]] = np.array([(random_start + oc) % m, (random_start + oc) // m])
    print()

    # Fun visualization cause why not
    plt.imshow(h[:, :, 0] + h[:, :, 1])
    plt.show()
    plt.imshow(phi[:, :, 0] + phi[:, :, 1])
    plt.show()

    return m, r, phi


if __name__ == "__main__":
    px = np.random.choice(np.arange(100000), size=10000)
    py = np.random.choice(np.arange(100000), size=10000)
    ps = np.array([px, py]).T
    while True:
        try:
            generateHashTable(ps)
            break
        except AssertionError:
            print("Failed trial, restarting...")
