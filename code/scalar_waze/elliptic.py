"""
secp256k1 Elliptic Curve implementation.

The Bitcoin/Ethereum elliptic curve: y² = x³ + 7 (mod p)

Holonomy connections:
- 7: curve constant term ✓
- 17: prime factor in τ₁ = 75/17 ✓
- 71: denominator of lemma = 75/71 ✓
"""

import numpy as np
from typing import Tuple, Optional


class Secp256k1Curve:
    """
    secp256k1 elliptic curve used in Bitcoin and Ethereum.
    
    Curve equation: y² = x³ + 7 (mod p)
    
    Connections to Scalar Waze holonomy:
    - Constant 7 is first holonomy value
    - Prime structure preserved throughout framework
    """
    
    # secp256k1 parameters
    # Prime field
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    
    # Curve parameters: y² = x³ + ax + b (mod p)
    A = 0  # Coefficient of x
    B = 7  # Constant term (holonomy connection!)
    
    # Generator point
    GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    
    # Order of generator point
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    
    def __init__(self):
        """Initialize secp256k1 curve."""
        self.p = self.P
        self.a = self.A
        self.b = self.B
        self.g = (self.GX, self.GY)
        self.n = self.N
    
    def is_on_curve(self, x: int, y: int) -> bool:
        """
        Check if point (x, y) is on the curve.
        
        Args:
            x, y: Point coordinates
            
        Returns:
            True if point satisfies y² = x³ + 7 (mod p)
        """
        left = (y * y) % self.p
        right = (x * x * x + self.b) % self.p
        return left == right
    
    def get_point(self, x: int) -> Tuple[int, int]:
        """
        Get a point on the curve for given x coordinate.
        
        Args:
            x: x-coordinate
            
        Returns:
            (x, y) point on curve, or raises ValueError if x not valid
        """
        x = x % self.p
        
        # Compute y² = x³ + 7 (mod p)
        y_squared = (pow(x, 3, self.p) + self.b) % self.p
        
        # Compute square root mod p (Tonelli-Shanks algorithm)
        y = self._sqrt_mod_p(y_squared)
        
        if y is None:
            raise ValueError(f"No point on curve for x = {x}")
        
        return (x, y)
    
    def _sqrt_mod_p(self, a: int) -> Optional[int]:
        """
        Compute square root of a modulo p using Tonelli-Shanks algorithm.
        
        Args:
            a: Value to find square root of
            
        Returns:
            Square root if exists, None otherwise
        """
        # For secp256k1, p ≡ 3 (mod 4), so we can use simple formula
        # y = a^((p+1)/4) mod p
        if pow(a, (self.p - 1) // 2, self.p) != 1:
            return None  # No square root exists
        
        y = pow(a, (self.p + 1) // 4, self.p)
        return y
    
    def point_add(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int]:
        """
        Add two points on the elliptic curve.
        
        Args:
            p1, p2: Points to add
            
        Returns:
            Sum point p1 + p2
        """
        if p1 == (0, 0):
            return p2
        if p2 == (0, 0):
            return p1
        
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                return self.point_double(p1)
            else:
                # Points are inverses
                return (0, 0)
        
        # Compute slope
        slope = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        
        # Compute result
        x3 = (slope * slope - x1 - x2) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_double(self, p: Tuple[int, int]) -> Tuple[int, int]:
        """
        Double a point on the elliptic curve.
        
        Args:
            p: Point to double
            
        Returns:
            Doubled point 2p
        """
        x, y = p
        
        if y == 0:
            return (0, 0)
        
        # Compute slope: (3x² + a) / (2y)
        slope = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
        
        # Compute result
        x3 = (slope * slope - 2 * x) % self.p
        y3 = (slope * (x - x3) - y) % self.p
        
        return (x3, y3)
    
    def scalar_mult(self, k: int, p: Tuple[int, int]) -> Tuple[int, int]:
        """
        Multiply point by scalar: k * p
        
        Args:
            k: Scalar multiplier
            p: Point to multiply
            
        Returns:
            Result point k*p
        """
        if k == 0:
            return (0, 0)
        if k == 1:
            return p
        
        # Binary method
        result = (0, 0)
        addend = p
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1
        
        return result
    
    def get_holonomy_connections(self) -> dict:
        """
        Get holonomy connections to the curve.
        
        Returns:
            Dictionary with connections to holonomy sequence
        """
        holonomy = [7, 17, 18, 71, 75, 126, 1275, 4412]
        
        return {
            'curve_equation': 'y² = x³ + 7 (mod p)',
            'constant_b': self.b,
            'holonomy_constant': holonomy[0],
            'connection_verified': self.b == holonomy[0],
            'holonomy_sequence': holonomy,
            'product_relations': {
                '7 × 18': 7 * 18,  # = 126
                '17 × 75': 17 * 75,  # = 1275
            },
            'prime_factors': {
                '17': 'prime in τ₁ = 75/17',
                '71': 'prime in lemma = 75/71',
                '7': 'curve constant and holonomy[0]',
            },
            'tau_1_ratio': 75 / 17,
            'lemma_ratio': 75 / 71,
        }
    
    def generate_holonomy_points(self) -> list:
        """
        Generate points on curve corresponding to holonomy values.
        
        Returns:
            List of points for x = holonomy values
        """
        holonomy = [7, 17, 18, 71, 75, 126, 1275, 4412]
        points = []
        
        for x in holonomy:
            try:
                point = self.get_point(x)
                points.append({
                    'holonomy_value': x,
                    'point': point,
                    'on_curve': self.is_on_curve(point[0], point[1])
                })
            except ValueError:
                points.append({
                    'holonomy_value': x,
                    'point': None,
                    'on_curve': False
                })
        
        return points
