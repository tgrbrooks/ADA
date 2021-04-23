

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def set_float(orig, value):
    if isfloat(value):
        return float(value)
    return orig


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def set_int(orig, value):
    if isint(value):
        return float(value)
    return orig
