from random import shuffle


def who_wins(b):
    if b[0][0] == b[0][1] == b[0][2]:
        return b[0][0]
    if b[1][0] == b[1][1] == b[1][2]:
        return b[1][0]
    if b[2][0] == b[2][1] == b[2][2]:
        return b[2][0]
    if b[0][0] == b[1][0] == b[2][0]:
        return b[0][0]
    if b[0][1] == b[1][1] == b[2][1]:
        return b[0][1]
    if b[0][2] == b[1][2] == b[2][2]:
        return b[0][2]
    if b[0][0] == b[1][1] == b[2][2]:
        return b[1][1]
    if b[0][2] == b[1][1] == b[2][0]:
        return b[1][1]
    return "_"


def hard_ia_turn(b, l_x, l_y, token):
    if l_x is None:
        return get_free(b)
    if not is_row_ok(b, l_y, token):
        return get_row_free(b, l_y)
    if not is_column_ok(b, l_x, token):
        return get_column_free(b, l_x)
    if not is_diagonal1_ok(b, token):
        return get_diagonal1_free(b)
    if not is_diagonal2_ok(b, token):
        return get_diagonal2_free(b)
    return get_free(b)


def medium_ia_turn(b, l_x, l_y, token):
    if l_x is None:
        return get_free(b)
    if not is_row_ok(b, l_y, token):
        return get_row_free(b, l_y)
    if not is_column_ok(b, l_x, token):
        return get_column_free(b, l_x)
    return get_free(b)


def dumb_ia_turn(b, l_x, l_y, token):
    return get_free(b)


def get_all():
    a = []
    for n in range(3):
        for m in range(3):
            a.append((n, m))
    return a


def get_free(b):
    a = get_all()
    shuffle(a)
    for x, y in a:
        if b[x][y] == "_":
            return x, y
    return None


def is_full(b):
    return not get_free(b)


def is_row_ok(b, y, token):
    for n in range(3):
        if b[n][y] == token:
            return True
    return False


def is_column_ok(b, x, token):
    for n in range(3):
        if b[x][n] == token:
            return True
    return False


def is_diagonal1_ok(b, token):
    for n in range(3):
        if b[n][n] == token:
            return True
    return False


def is_diagonal2_ok(b, token):
    for n in range(3):
        if b[n][2-n] == token:
            return True
    return False


def get_row_free(b, y):
    for n in range(3):
        if b[n][y] == "_":
            return (n, y)
    return None


def get_column_free(b, x):
    for n in range(3):
        if b[x][n] == "_":
            return (x, n)
    return None


def get_diagonal1_free(b):
    for n in range(3):
        if b[n][n] == "_":
            return (n, n)
    return None


def get_diagonal2_free(b):
    for n in range(3):
        if b[n][2-n] == "_":
            return (n, 2-n)
    return None