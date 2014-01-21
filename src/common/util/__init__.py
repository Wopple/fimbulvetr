def combinations(list):
    size = len(list)
    if size < 2:
        raise RuntimeError, "combinations takes a list of size >= 2"

    for i in xrange(size - 1):
        for j in xrange(i + 1, size):
            yield (list[i], list[j])

def exclusiveKeys(k1, k2):
    if k1 and k2:
        k1 = False
        k2 = False
    return k1, k2
