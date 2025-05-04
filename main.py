import sympy
import numpy as np
import matplotlib.pyplot as plt

def generateHashTable(points):
    n = len(points)
    print(f"{n=}")
    m = int(sympy.nextprime(np.sqrt(n * 1.01)))  #type:ignore
    print(f"{m=}")
    increment_factor = 1.2
    r = int(np.sqrt(n) / 2)
    print(f"Initial {r=}")

    h0 = np.array(points % m, dtype="int64")
    h1 = np.array(points % r, dtype="int64")

    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    while len(phashes) != n:
        print(f"Trying {r=}", end="\r", flush=True)
        r = int(r * increment_factor)
        h1 = np.array(points % r, dtype="int64")
        phashes = np.unique(np.column_stack((h0, h1)), axis=0)

    h1 = np.array(points % r, dtype="int64")
    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"Settled on {r=}")

    groups = [phashes[np.all(phashes[:, 2:] == k, axis=1)] for k in np.unique(h1, axis=0)][::-1]

    phi = np.zeros((r, r, 2), dtype="int64")
    h = np.zeros((m, m, 2), dtype="int64") - 1

    i = 0
    oc = 0
    while i < len(groups):
        g = groups[i]                         # shape: (G, N)
        k12 = g[:, :2]                        # shape: (G, 2)
        phi_lookup = phi[g[:, 3], g[:, 2]]   # shape: (G, 2)
        ghs = (k12 + phi_lookup) % m         # shape: (G, 2)

        # Lookup in h using computed hashes
        selected = h[ghs[:, 1], ghs[:, 0]]   # shape: (G, 2)
        valid = not np.any(np.all(selected != [-1, -1], axis=1))  # If ANY already-filled slot exists, invalid

        if valid:
            # Update h[gh[1], gh[0]] = g[:2] in bulk
            h[ghs[:, 1], ghs[:, 0]] = g[:, :2]
            i += 1
            oc = 0
            random_start = np.random.randint(0, r**2 - 1)
        else:
            offseti = g[0, 2:]  # (k[2], k[3]) in order (x, y)
            oc += 1
            assert oc < m**2, "oc exploded"
            phi[offseti[1], offseti[0]] = np.array([(random_start + oc) % m, (random_start + oc) // m])

    # Fun visualization cause why not
    plt.imshow((h[:, :, 0] != -1) & (h[:, :, 1] != -1))
    plt.show()
    plt.imshow((phi[:, :, 0] != 0) & (phi[:, :, 1] != 0))
    plt.show()

    return m, r, phi


if __name__ == "__main__":
    px = np.random.choice(np.arange(1000), size=1000)
    py = np.random.choice(np.arange(1000), size=1000)
    ps = np.array([px, py]).T
    i=15
    while (i>=0):
        try:
            generateHashTable(ps)
            break
        except AssertionError:
            print(f"Failed trial {15-i}, restarting...")
            i -= 1
    else:
        print("Finished all trials")

