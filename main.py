from sympy import gcd
import numpy as np
import matplotlib.pyplot as plt


def generateHashTable(points):
    n = len(points)
    m = int(np.sqrt(n) if n < 256 else np.sqrt(1.01 * n)) + 1
    r = int(np.sqrt(n) / 4) + 1
    print(f"Initial {r=}")

    h0 = np.array(points % m, dtype="int64")
    h1 = np.array(points % r, dtype="int64")

    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"{len(phashes)=}")
    while len(phashes) != n:
        r += 1
        assert r <= m, "R blew up"

        print(f"Trying {r=}")
        if (int(gcd(m, r)) not in [1, r]): #type:ignore
            print(f"Invalid {gcd(m, r) = }, {m} {r}")
            continue
        print(f"{len(phashes)=}")

        h1 = np.array(points % r, dtype="int64")
        phashes = np.unique(np.column_stack((h0, h1)), axis=0)

    h1 = np.array(points % r, dtype="int64")
    phashes = np.unique(np.column_stack((h0, h1)), axis=0)
    print(f"Settled on {r=}")

    groups = [phashes[np.all(phashes[:, 2:] == k, axis=1)] for k in np.unique(h1, axis=0)]
    groups.sort(key=len)

    while True:
        try:
            phi = np.zeros((r, r, 2), dtype="int64") - 1
            h = np.zeros((m, m, 2), dtype="int64") - 1

            i = 1
            oc = 0
            while i <= len(groups):
                g = groups[-i]                         # shape: (G, N)
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
                    random_start = np.random.randint(0, m**2 - 1)
                    # print(f"Start: {oc=}, {random_start=}")
                else:
                    offseti = g[0, 2:]  # (k[2], k[3]) in order (x, y)
                    oc += 1
                    assert oc <= m**2, "OC Exploded"
                    phi[offseti[1], offseti[0]] = np.array([(random_start + oc) % m, ((random_start + oc) // m) % m])
                    # print(f"({(random_start + oc) % m = }, {((random_start + oc) // m) % m = }), {oc=} {m=}")

            break
        except AssertionError:
            pass


    print(f"{n=}")
    print(f"{m=}")
    print(f"{r=}")
    # Fun visualization cause why not
    plt.imshow((h[:, :, 0] != -1) & (h[:, :, 1] != -1))
    plt.show()
    plt.imshow((phi[:, :, 0] != -1) & (phi[:, :, 1] != -1))
    plt.show()

    return m, r, phi

GRIDSIZE = 5000
POINTS = 5000
if __name__ == "__main__":
    ps = np.arange(GRIDSIZE ** 2)
    np.random.shuffle(ps)
    ps = ps[:POINTS]
    points = np.array([[x%GRIDSIZE, x//GRIDSIZE] for x in ps])
    assert len(points) == len(np.unique(points, axis=0)), "Input Invalid"
    print(f"{ps=}")
    print(f"{points=}")
    generateHashTable(points)

