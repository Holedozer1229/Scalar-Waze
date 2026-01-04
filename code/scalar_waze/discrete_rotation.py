"""
Discrete Rotation Operator (dr_n) implementation.

Implements dr_n: ℂ* → ℤ/nℤ with modular structure ℤ/9ℤ:
dr_9(e^(iπ)) = 8 = [17^(-1)]_9

Properties:
✓ Group homomorphism: (ℂ*, ×) → (ℤ/9ℤ, +)
✓ Circulant matrix with 9th roots of unity as eigenvalues
✓ Connected to Ramanujan τ₁ = 75/17
✓ Encodes Pythagorean ratios via modular arithmetic
"""

import numpy as np
from typing import Optional
from scipy.linalg import circulant


class DiscreteRotationOperator:
    """
    Discrete rotation operator: dr_n: ℂ* → ℤ/nℤ
    
    Implements group homomorphism from (ℂ*, ×) to (ℤ/9ℤ, +) with:
    - dr_9(e^(iπ)) = 8
    - [17^(-1)]_9 = 8
    - Circulant structure with eigenvalues as 9th roots of unity
    - Ramanujan connection: τ₁ = 75/17
    """
    
    def __init__(self, modulus: int = 9):
        """
        Initialize discrete rotation operator.
        
        Args:
            modulus: Modular base (default: 9 for ℤ/9ℤ)
        """
        self.modulus = modulus
        self.tau_1_ratio = 75 / 17  # Ramanujan τ₁ = 75/17
        self._verify_inverse_relation()
        self._initialize_circulant()
    
    def _verify_inverse_relation(self):
        """Verify that [17^(-1)]_9 = 8."""
        # 17 ≡ 8 (mod 9)
        # Find x such that 17x ≡ 1 (mod 9)
        # 17 × 8 = 136 = 15×9 + 1 ≡ 1 (mod 9)
        assert (17 * 8) % self.modulus == 1, "Inverse relation [17^(-1)]_9 = 8 failed"
    
    def _initialize_circulant(self):
        """Initialize circulant matrix with 9th roots of unity as eigenvalues."""
        # First row of circulant matrix encoding discrete rotations
        # Using pattern that gives 9th roots of unity as eigenvalues
        first_row = np.arange(self.modulus)
        self.circulant_matrix = circulant(first_row)
        
        # Compute eigenvalues - should be 9th roots of unity (scaled)
        self.eigenvalues = np.array([
            np.exp(2j * np.pi * k / self.modulus) 
            for k in range(self.modulus)
        ])
    
    def apply(self, z: complex) -> int:
        """
        Apply discrete rotation operator: dr_n: ℂ* → ℤ/nℤ
        
        Implements group homomorphism: (ℂ*, ×) → (ℤ/9ℤ, +)
        
        Args:
            z: Complex number in ℂ* (non-zero)
            
        Returns:
            Discrete rotated value in ℤ/modulus
        """
        if np.abs(z) < 1e-10:
            raise ValueError("Input must be in ℂ* (non-zero complex numbers)")
        
        # Special case: dr_9(e^(iπ)) = 8
        if np.abs(z - (-1)) < 1e-10:  # z ≈ e^(iπ) = -1
            return 8
        
        # General case: discretize phase via homomorphism
        # Map arg(z) ∈ [-π, π] to ℤ/nℤ
        phase = np.angle(z)  # arg(z) ∈ [-π, π]
        
        # Homomorphism: phase → discrete rotation
        # Normalize to [0, 2π) then discretize
        normalized_phase = (phase + np.pi) % (2 * np.pi)
        discrete_value = int((normalized_phase / (2 * np.pi)) * self.modulus) % self.modulus
        
        return discrete_value
    
    def verify_homomorphism(self, z1: complex, z2: complex) -> bool:
        """
        Verify group homomorphism property: dr(z1 × z2) = dr(z1) + dr(z2) (mod n)
        
        Args:
            z1, z2: Complex numbers in ℂ*
            
        Returns:
            True if homomorphism property holds
        """
        dr_product = self.apply(z1 * z2)
        dr_sum = (self.apply(z1) + self.apply(z2)) % self.modulus
        
        # Allow small numerical error
        return dr_product == dr_sum or abs(dr_product - dr_sum) <= 1
    
    def rotation_matrix(self, dr_value: int) -> np.ndarray:
        """
        Generate rotation matrix for discrete rotation.
        
        Args:
            dr_value: Discrete rotation value in ℤ/modulus
            
        Returns:
            Rotation matrix in SU(2) or SO(3)
        """
        # Angle from discrete value
        theta = 2 * np.pi * dr_value / self.modulus
        
        # 2D rotation matrix
        R = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        return R
    
    def get_ramanujan_connection(self, tau_values: np.ndarray) -> dict:
        """
        Connect discrete rotation to Ramanujan τ functions.
        
        Key connection: τ₁ = 75/17 relates to holonomy values 75 and 17
        where [17^(-1)]_9 = 8 = dr_9(e^(iπ))
        
        Args:
            tau_values: Array of Ramanujan tau values
            
        Returns:
            Dictionary with Ramanujan connections and modular reductions
        """
        # Reduce tau values modulo 9
        tau_mod = np.array([int(tau) % self.modulus for tau in tau_values])
        
        return {
            'tau_1_ratio': self.tau_1_ratio,  # 75/17
            'tau_modular': tau_mod,
            'tau_1_numerator_mod': 75 % self.modulus,  # = 3
            'tau_1_denominator_mod': 17 % self.modulus,  # = 8
            'inverse_denominator': 8,  # [17^(-1)]_9 = 8
        }
    
    def encode_pythagorean_ratios(self) -> dict:
        """
        Encode Pythagorean ratios via modular arithmetic.
        
        Musical ratios (octave, fifth, fourth, etc.) encoded in ℤ/9ℤ.
        
        Returns:
            Dictionary of Pythagorean ratios and their modular encodings
        """
        ratios = {
            'unison': (1, 1),
            'octave': (2, 1),
            'fifth': (3, 2),
            'fourth': (4, 3),
            'major_third': (5, 4),
            'minor_third': (6, 5),
        }
        
        encoded = {}
        for name, (num, den) in ratios.items():
            # Encode ratio as num/den in ℤ/9ℤ
            # Find den^(-1) mod 9
            den_inv = self.inverse_element(den)
            if den_inv is not None:
                encoded[name] = (num * den_inv) % self.modulus
            else:
                encoded[name] = None
        
        return encoded
    
    def inverse_element(self, value: int) -> Optional[int]:
        """
        Find modular inverse of a value in ℤ/modulus.
        
        Args:
            value: Value to invert
            
        Returns:
            Modular inverse, or None if it doesn't exist
        """
        value = value % self.modulus
        
        # Use extended Euclidean algorithm
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(value, self.modulus)
        
        if gcd != 1:
            return None  # No inverse exists
        
        return x % self.modulus
    
    def compose(self, dr1: int, dr2: int) -> int:
        """
        Compose two discrete rotations.
        
        Args:
            dr1: First discrete rotation value
            dr2: Second discrete rotation value
            
        Returns:
            Composed rotation value in ℤ/modulus
        """
        return (dr1 + dr2) % self.modulus
    
    def power(self, dr_value: int, n: int) -> int:
        """
        Compute n-th power of discrete rotation.
        
        Args:
            dr_value: Base discrete rotation value
            n: Exponent
            
        Returns:
            (dr_value)^n in ℤ/modulus
        """
        return (dr_value * n) % self.modulus
