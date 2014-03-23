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

def makeByte(*bits):
    """
    Converts up to 8
    """

    if len(bits) > 8:
        raise RuntimeError, "Too many bits: " + len(bits)

    byte = 0

    for i, b in enumerate(bits):
        byte |= int(b) << i

    return byte

def byteToList(byte):
    l = []

    for i in xrange(8):
        l.append(byte & (1 << i) > 0)
