import math

def simplify_ratio(width, height):
    gcd = math.gcd(width, height)
    return (width // gcd, height // gcd)