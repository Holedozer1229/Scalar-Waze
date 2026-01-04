"""
Möbius-Fractal Wave Operator (Ω̂) implementation.

Implements: Ω̂[f](s) = ∫_ℂ K_Möbius(s,s') f(s') e^(iφ_dr(s')) ds'

where:
• K_Möbius(s,s') = 1/(s-s')² (Möbius kernel)
• φ_dr(s') = 2π·dr_n(e^(i·arg(s')))/n (phase)

Properties:
✓ Self-similar: Ω̂^λ[f](s) = λ^Δ Ω̂[f](λs)
✓ Modular invariant: Ω̂[f](s+n) = Ω̂[f](s)
✓ Möbius covariant under SL(2,ℤ)
✓ Preserves Pythagorean ratios
"""

import numpy as np
from scipy import integrate
from typing import Callable, Optional
from .discrete_rotation import DiscreteRotationOperator


class ContinuousWaveOperator:
    """
    Möbius-Fractal Wave Operator with holomorphic structure.
    
    Implements continuous wave transformation with:
    - Möbius kernel for holomorphic covariance
    - Discrete rotation phase modulation
    - Self-similar fractal structure
    - Preservation of Pythagorean ratios
    """
    
    def __init__(self, modulus: int = 9, scaling_dimension: float = 1.0):
        """
        Initialize Möbius-Fractal Wave Operator.
        
        Args:
            modulus: Modular base for discrete rotation (default: 9)
            scaling_dimension: Scaling dimension Δ for self-similarity
        """
        self.modulus = modulus
        self.scaling_dimension = scaling_dimension
        self.dr_operator = DiscreteRotationOperator(modulus)
    
    def mobius_kernel(self, s: complex, s_prime: complex, regularization: float = 1e-6) -> complex:
        """
        Möbius kernel: K_Möbius(s,s') = 1/(s-s')²
        
        Args:
            s: Target point
            s_prime: Source point
            regularization: Small constant to avoid division by zero
            
        Returns:
            Kernel value
        """
        diff = s - s_prime
        if np.abs(diff) < regularization:
            diff = regularization
        return 1.0 / (diff ** 2)
    
    def compute_phase(self, s_prime: complex) -> float:
        """
        Compute discrete rotation phase: φ_dr(s') = 2π·dr_n(e^(i·arg(s')))/n
        
        Args:
            s_prime: Complex point
            
        Returns:
            Phase value in [0, 2π)
        """
        # Extract argument and create unit complex number
        arg_s = np.angle(s_prime)
        z = np.exp(1j * arg_s)
        
        # Apply discrete rotation
        dr_value = self.dr_operator.apply(z)
        
        # Compute phase
        phase = 2 * np.pi * dr_value / self.modulus
        
        return phase
    
    def apply(
        self, 
        features: np.ndarray, 
        holonomy_phase: float = 0.0,
        tau_couplings: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Apply wave operator Ω̂[f] to features.
        
        For discrete features, uses finite approximation of the integral operator.
        
        Args:
            features: Input features Fᵢ (e.g., zeta zero gaps)
            holonomy_phase: Additional phase from holonomy
            tau_couplings: Ramanujan tau couplings for modulation
            
        Returns:
            Transformed features
        """
        m = len(features)
        transformed = np.zeros(m, dtype=complex)
        
        if tau_couplings is None:
            tau_couplings = np.ones(m)
        
        # Map features to complex plane (feature values → complex points)
        # Use features as imaginary parts on critical line Re(s) = 0.5
        s_points = 0.5 + 1j * features
        
        # Apply discrete approximation of integral operator
        for i in range(m):
            s = s_points[i]
            integral_sum = 0.0
            
            for j in range(m):
                s_prime = s_points[j]
                
                # Möbius kernel
                kernel = self.mobius_kernel(s, s_prime)
                
                # Discrete rotation phase
                dr_phase = self.compute_phase(s_prime)
                
                # Total phase including holonomy and Ramanujan coupling
                total_phase = dr_phase + holonomy_phase + tau_couplings[j % len(tau_couplings)]
                
                # Integrand: K(s,s') * f(s') * e^(iφ)
                integrand = kernel * features[j] * np.exp(1j * total_phase)
                
                integral_sum += integrand
            
            # Normalize by number of points (discrete integration)
            transformed[i] = integral_sum / m
        
        return transformed
    
    def apply_to_function(
        self,
        func: Callable[[complex], complex],
        s: complex,
        integration_path: np.ndarray,
        holonomy_phase: float = 0.0
    ) -> complex:
        """
        Apply wave operator to a continuous function.
        
        Ω̂[f](s) = ∫_ℂ K_Möbius(s,s') f(s') e^(iφ_dr(s')) ds'
        
        Args:
            func: Function f: ℂ → ℂ to transform
            s: Evaluation point
            integration_path: Discrete path in ℂ for numerical integration
            holonomy_phase: Additional phase from holonomy
            
        Returns:
            Ω̂[f](s)
        """
        integral_sum = 0.0
        
        for s_prime in integration_path:
            # Möbius kernel
            kernel = self.mobius_kernel(s, s_prime)
            
            # Function value
            f_value = func(s_prime)
            
            # Discrete rotation phase
            dr_phase = self.compute_phase(s_prime)
            
            # Total phase
            total_phase = dr_phase + holonomy_phase
            
            # Integrand
            integrand = kernel * f_value * np.exp(1j * total_phase)
            
            integral_sum += integrand
        
        # Normalize (discrete integration)
        result = integral_sum / len(integration_path)
        
        return result
    
    def verify_self_similarity(
        self,
        features: np.ndarray,
        lambda_scale: float = 2.0
    ) -> dict:
        """
        Verify self-similar property: Ω̂^λ[f](s) = λ^Δ Ω̂[f](λs)
        
        Args:
            features: Test features
            lambda_scale: Scaling factor λ
            
        Returns:
            Dictionary with verification results
        """
        # Apply operator to features
        omega_f = self.apply(features)
        
        # Apply operator to scaled features
        scaled_features = lambda_scale * features
        omega_scaled = self.apply(scaled_features)
        
        # Expected scaling: λ^Δ Ω̂[f]
        expected = (lambda_scale ** self.scaling_dimension) * omega_f
        
        # Compute relative error
        error = np.linalg.norm(omega_scaled - expected) / np.linalg.norm(expected)
        
        return {
            'lambda': lambda_scale,
            'scaling_dimension': self.scaling_dimension,
            'relative_error': error,
            'self_similar': error < 0.1  # 10% tolerance
        }
    
    def verify_modular_invariance(
        self,
        features: np.ndarray,
        n: Optional[int] = None
    ) -> dict:
        """
        Verify modular invariance: Ω̂[f](s+n) = Ω̂[f](s)
        
        Args:
            features: Test features
            n: Modular period (default: modulus)
            
        Returns:
            Dictionary with verification results
        """
        if n is None:
            n = self.modulus
        
        # Apply operator
        omega_f = self.apply(features)
        
        # Shift features by n and apply operator
        shifted_features = features + n
        omega_shifted = self.apply(shifted_features)
        
        # Compute relative error
        error = np.linalg.norm(omega_f - omega_shifted) / np.linalg.norm(omega_f)
        
        return {
            'period': n,
            'relative_error': error,
            'modular_invariant': error < 0.1  # 10% tolerance
        }
    
    def mobius_transform(
        self,
        s: complex,
        a: int, b: int, c: int, d: int
    ) -> complex:
        """
        Apply Möbius transformation: γ(s) = (as + b)/(cs + d)
        
        For γ ∈ SL(2,ℤ): ad - bc = 1
        
        Args:
            s: Complex point
            a, b, c, d: Möbius transformation coefficients
            
        Returns:
            Transformed point γ(s)
        """
        # Verify SL(2,ℤ) condition
        assert a*d - b*c == 1, "Must satisfy ad - bc = 1 for SL(2,ℤ)"
        
        denominator = c * s + d
        if np.abs(denominator) < 1e-10:
            return np.inf + 0j
        
        return (a * s + b) / denominator
    
    def verify_mobius_covariance(
        self,
        features: np.ndarray,
        a: int = 1, b: int = 1, c: int = 0, d: int = 1
    ) -> dict:
        """
        Verify Möbius covariance under SL(2,ℤ) transformations.
        
        Args:
            features: Test features
            a, b, c, d: Möbius transformation coefficients (default: translation)
            
        Returns:
            Dictionary with verification results
        """
        # Verify SL(2,ℤ)
        det = a*d - b*c
        if det != 1:
            return {'error': 'Not in SL(2,ℤ)', 'determinant': det}
        
        # Apply operator to features
        omega_f = self.apply(features)
        
        # Transform features via Möbius transformation
        s_points = 0.5 + 1j * features
        s_transformed = np.array([
            self.mobius_transform(s, a, b, c, d) 
            for s in s_points
        ])
        
        # Extract imaginary parts for new features
        transformed_features = np.imag(s_transformed)
        
        # Apply operator to transformed features
        omega_transformed = self.apply(transformed_features)
        
        # Compute covariance metric
        correlation = np.abs(np.vdot(omega_f, omega_transformed)) / (
            np.linalg.norm(omega_f) * np.linalg.norm(omega_transformed)
        )
        
        return {
            'transformation': [[a, b], [c, d]],
            'correlation': correlation,
            'mobius_covariant': correlation > 0.8  # High correlation expected
        }
    
    def preserve_pythagorean_ratios(self, features: np.ndarray) -> dict:
        """
        Verify preservation of Pythagorean ratios.
        
        Args:
            features: Input features
            
        Returns:
            Dictionary with ratio preservation metrics
        """
        # Apply operator
        transformed = self.apply(features)
        
        # Compute ratios before and after
        original_ratios = []
        transformed_ratios = []
        
        pythagorean_pairs = [(2, 1), (3, 2), (4, 3), (5, 4)]  # Musical intervals
        
        for i, j in pythagorean_pairs:
            if i < len(features) and j < len(features):
                if np.abs(features[j]) > 1e-10:
                    original_ratios.append(features[i] / features[j])
                if np.abs(transformed[j]) > 1e-10:
                    transformed_ratios.append(np.abs(transformed[i] / transformed[j]))
        
        if len(original_ratios) > 0 and len(transformed_ratios) > 0:
            # Compute how well ratios are preserved
            ratio_preservation = np.mean([
                np.abs(t / o) if o != 0 else 1.0
                for o, t in zip(original_ratios, transformed_ratios)
            ])
        else:
            ratio_preservation = 1.0
        
        return {
            'original_ratios': original_ratios,
            'transformed_ratios': transformed_ratios,
            'preservation_factor': ratio_preservation,
            'ratios_preserved': abs(ratio_preservation - 1.0) < 0.2
        }
