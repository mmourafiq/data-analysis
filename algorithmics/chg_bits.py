# setBit() returns an integer with the bit at 'offset' set to 1.    
def setBit(int_type, offset):
    mask = 1 << offset
    return (int_type | mask)


# clearBit() returns an integer with the bit at 'offset' cleared. 
def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return (int_type & mask)


def set_bit(ind, val, int_type):
    return clearBit(int_type, ind) if val == "0" else setBit(int_type, ind)


def get_c(inx, A, B, n):
    res = A + B
    mask = 1 << inx
    return '1' if (res & mask) else '0'


def chg_bit():
    N, Q = [int(x) for x in raw_input().split()]
    A = int(raw_input(), 2)
    B = int(raw_input(), 2)
    result = ""
    while Q > 0:
        q = [x for x in raw_input().split()]
        if len(q) == 2:  # get operation
            result += get_c(int(q[1]), A, B, N + 1)
        elif q[0] == "set_a":
            A = set_bit(int(q[1]), q[2], A)
        else:
            B = set_bit(int(q[1]), q[2], B)
        Q -= 1
    print result


chg_bit()
