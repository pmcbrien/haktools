import random
import math
import sympy
import gmpy2
from gmpy2 import mpz, gcd, is_prime

# Pollard's p-1
def pollards_p_minus_1(n, B=10000):
    a = mpz(2)
    for j in range(2, B):
        a = gmpy2.powmod(a, j, n)
        d = gmpy2.gcd(a - 1, n)
        if 1 < d < n:
            return int(d)
    return None

# Lenstra's ECM (basic version)
def lenstra_ecm(n, max_tries=50, B=50):
    for _ in range(max_tries):
        x = random.randint(1, n-1)
        y = random.randint(1, n-1)
        a = random.randint(1, n-1)
        b = (y*y - x*x*x - a*x) % n
        curve = lambda x: (x*x*x + a*x + b) % n
        try:
            for j in range(2, B):
                x = (x*x - 2) % n
                d = gcd(x, n)
                if 1 < d < n:
                    return d
        except:
            continue
    return None

# Sophie Germain filter (helps for small primes)
def is_sophie_germain(p):
    return is_prime(p) and is_prime(2*p + 1)

# Hensel's Lemma (used to lift roots mod p to mod p^k)
def hensel_lift(f, x0, p, k):
    x = x0
    for i in range(1, k):
        fx = f(x)
        fpx = sympy.diff(f, sympy.symbols('x')).subs('x', x)
        if fpx % p == 0:
            return None
        e = (-fx * pow(fpx, -1, p)) % p
        x = (x + e * pow(p, i)) % pow(p, i+1)
    return x

# Main factoring orchestrator
def factor_semiprime(n):
    print(f"Factoring {n}...")
    if is_prime(n):
        print("Number is prime!")
        return [n]

    # Step 1: Trial division for very small factors
    for p in sympy.primerange(2, 1000):
        if n % p == 0:
            return [p, n // p]

    # Step 2: Pollard's p-1
    f = pollards_p_minus_1(n)
    if f:
        return [f, n // f]

    # Step 3: Lenstra ECM
    f = lenstra_ecm(n)
    if f:
        return [f, n // f]

    # Step 4: Check for Sophie Germain properties
    factors = sympy.factorint(n)
    for p in factors:
        if is_sophie_germain(p):
            print(f"{p} is a Sophie Germain prime.")
            return [p, n // p]

    # Step 5: GNFS stub
    print("General Number Field Sieve is not implemented (too complex).")

    return ["Failed to factor with current methods."]

# Example usage
if __name__ == "__main__":
    n = 589 * 593  # Small semiprime
    result = factor_semiprime(n)
    print("Factors:", result)
