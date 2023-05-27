def clip(x, min, max):
    assert min <= max
    
    if x < min:
        return min
    elif x > max:
        return max
    return x

def bound(x, bound):
    assert bound >= 0
    
    return clip(x, -bound, bound)