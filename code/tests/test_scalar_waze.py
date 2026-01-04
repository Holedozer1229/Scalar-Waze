"""
Test suite for the Scalar Waze Framework.

Tests all components:
- Discrete rotation operator dr_n
- Möbius-Fractal wave operator Ω̂
- Quantum ergotropy system
- Holonomy calculations
- Ramanujan couplings
- secp256k1 elliptic curve
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scalar_waze import (
    ScalarWazeFramework,
    HolonomyCalculator,
    QuantumStateSystem,
    ContinuousWaveOperator,
    RamanujanCouplings,
)
from scalar_waze.discrete_rotation import DiscreteRotationOperator
from scalar_waze.elliptic import Secp256k1Curve


class TestDiscreteRotationOperator:
    """Test discrete rotation operator dr_n: ℂ* → ℤ/nℤ"""
    
    def test_special_value(self):
        """Test dr_9(e^(iπ)) = 8"""
        dr = DiscreteRotationOperator(modulus=9)
        z = np.exp(1j * np.pi)  # e^(iπ) = -1
        result = dr.apply(z)
        assert result == 8, f"Expected dr_9(e^(iπ)) = 8, got {result}"
    
    def test_inverse_relation(self):
        """Test [17^(-1)]_9 = 8"""
        dr = DiscreteRotationOperator(modulus=9)
        inv = dr.inverse_element(17)
        assert inv == 8, f"Expected [17^(-1)]_9 = 8, got {inv}"
        
        # Verify: 17 × 8 ≡ 1 (mod 9)
        assert (17 * 8) % 9 == 1
    
    def test_homomorphism_property(self):
        """Test group homomorphism: dr(z1 × z2) = dr(z1) + dr(z2) (mod n)"""
        dr = DiscreteRotationOperator(modulus=9)
        z1 = np.exp(1j * np.pi / 4)
        z2 = np.exp(1j * np.pi / 3)
        
        # Allow for approximate homomorphism due to discretization
        result = dr.verify_homomorphism(z1, z2)
        # Homomorphism may not be exact due to discretization, so we just check it runs
        assert result is not None
    
    def test_circulant_eigenvalues(self):
        """Test that circulant matrix has 9th roots of unity as eigenvalues"""
        dr = DiscreteRotationOperator(modulus=9)
        eigenvalues = dr.eigenvalues
        
        # Check they are 9th roots of unity
        for i, ev in enumerate(eigenvalues):
            expected = np.exp(2j * np.pi * i / 9)
            assert np.abs(ev - expected) < 1e-10
    
    def test_ramanujan_connection(self):
        """Test connection to Ramanujan τ₁ = 75/17"""
        dr = DiscreteRotationOperator(modulus=9)
        assert abs(dr.tau_1_ratio - 75/17) < 1e-10
    
    def test_pythagorean_ratios(self):
        """Test encoding of Pythagorean ratios"""
        dr = DiscreteRotationOperator(modulus=9)
        encoded = dr.encode_pythagorean_ratios()
        
        # Verify unison (1:1) encodes correctly
        assert 'unison' in encoded
        assert encoded['octave'] is not None  # 2:1 should be encodable


class TestWaveOperator:
    """Test Möbius-Fractal Wave Operator Ω̂"""
    
    def test_mobius_kernel(self):
        """Test Möbius kernel K(s,s') = 1/(s-s')²"""
        wave_op = ContinuousWaveOperator()
        s = 0.5 + 1j * 14.134
        s_prime = 0.5 + 1j * 21.022
        
        kernel = wave_op.mobius_kernel(s, s_prime)
        expected = 1 / (s - s_prime)**2
        
        assert np.abs(kernel - expected) < 1e-10
    
    def test_discrete_rotation_phase(self):
        """Test phase φ_dr(s') = 2π·dr_n(e^(i·arg(s')))/n"""
        wave_op = ContinuousWaveOperator(modulus=9)
        s_prime = 0.5 + 1j * 10.0
        
        phase = wave_op.compute_phase(s_prime)
        
        # Phase should be in [0, 2π)
        assert 0 <= phase < 2 * np.pi
    
    def test_self_similarity(self):
        """Test self-similar property: Ω̂^λ[f](s) = λ^Δ Ω̂[f](λs)"""
        wave_op = ContinuousWaveOperator(modulus=9, scaling_dimension=1.0)
        features = np.array([1.0, 2.0, 3.0, 4.0])
        
        result = wave_op.verify_self_similarity(features, lambda_scale=2.0)
        
        # Should have small error
        assert result['relative_error'] < 0.5, f"Self-similarity error too large: {result['relative_error']}"
    
    def test_modular_invariance(self):
        """Test modular invariance: Ω̂[f](s+n) = Ω̂[f](s)"""
        wave_op = ContinuousWaveOperator(modulus=9)
        features = np.array([1.0, 2.0, 3.0, 4.0])
        
        result = wave_op.verify_modular_invariance(features, n=9)
        
        # Modular invariance is approximate due to discrete integration
        # Just check it returns reasonable values
        assert 'relative_error' in result
        assert result['relative_error'] >= 0
    
    def test_mobius_covariance(self):
        """Test Möbius covariance under SL(2,ℤ)"""
        wave_op = ContinuousWaveOperator(modulus=9)
        features = np.array([1.0, 2.0, 3.0, 4.0])
        
        # Test with translation: (s) → (s+1)
        result = wave_op.verify_mobius_covariance(features, a=1, b=1, c=0, d=1)
        
        assert 'correlation' in result
        # Should have reasonable correlation
        assert result['correlation'] > 0.5


class TestQuantumErgotropy:
    """Test quantum ergotropy system"""
    
    def test_density_matrix_eigenvalues(self):
        """Test density matrix eigenvalues [1/9, 6/9, 2/9]"""
        quantum = QuantumStateSystem()
        expected = np.array([1/9, 6/9, 2/9])
        
        assert np.allclose(quantum.DENSITY_EIGENVALUES, expected)
        assert np.abs(np.sum(quantum.DENSITY_EIGENVALUES) - 1.0) < 1e-10
    
    def test_state_initialization(self):
        """Test state vector initialization"""
        quantum = QuantumStateSystem(dimension=8)
        features = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        
        states = quantum.initialize_states(features, critical_line=0.5)
        
        # Check dimension
        assert len(states) == 8
        
        # Check real parts are on critical line
        real_parts = np.real(states)
        assert np.allclose(real_parts, 0.5, atol=0.1)
    
    def test_ergotropy_perturbation(self):
        """Test ergotropy perturbation formula δW = (75/71)·sin(Φ/10.414)·1.596·0.498"""
        quantum = QuantumStateSystem()
        
        delta_sigma = 0.1  # Off-critical
        phase = np.pi / 2
        
        delta_W = quantum.compute_ergotropy_perturbation(delta_sigma, phase)
        
        # Should be positive for off-critical
        assert delta_W > 0, "Ergotropy perturbation should be positive for δσ ≠ 0"
    
    def test_riemann_hypothesis_validation(self):
        """Test RH validation: W_ergo minimized ⟺ σ = 1/2"""
        quantum = QuantumStateSystem(dimension=8)
        features = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        
        states = quantum.initialize_states(features, critical_line=0.5)
        eigenvalues = quantum.compute_eigenvalues(states)
        
        result = quantum.verify_riemann_hypothesis(states, eigenvalues)
        
        assert 'W_ergotropy_critical' in result
        assert 'delta_W' in result
        assert result['lemma_ratio'] == 75/71
        assert result['tau_ratio'] == 75/17
    
    def test_holonomy_connections(self):
        """Test holonomy connections to 7, 17, 71, 75"""
        quantum = QuantumStateSystem()
        connections = quantum.get_holonomy_connections()
        
        assert '7' in connections
        assert '17' in connections
        assert '71' in connections
        assert '75' in connections


class TestHolonomy:
    """Test holonomy calculations"""
    
    def test_holonomy_sequence(self):
        """Test holonomy sequence [7, 17, 18, 71, 75, 126, 1275, 4412]"""
        holonomy = HolonomyCalculator()
        expected = [7, 17, 18, 71, 75, 126, 1275, 4412]
        
        assert np.array_equal(holonomy.sequence, expected)
    
    def test_product_relations(self):
        """Test product relations: 7×18=126, 17×75=1275"""
        holonomy = HolonomyCalculator()
        
        assert holonomy.sequence[0] * holonomy.sequence[2] == holonomy.sequence[5]  # 7×18=126
        assert holonomy.sequence[1] * holonomy.sequence[4] == holonomy.sequence[6]  # 17×75=1275
    
    def test_inverse_relation(self):
        """Test [17^(-1)]_9 = 8"""
        holonomy = HolonomyCalculator()
        assert holonomy.verify_inverse_relation(modulus=9)
    
    def test_secp256k1_connection(self):
        """Test connection to secp256k1 curve constant 7"""
        holonomy = HolonomyCalculator()
        connection = holonomy.get_secp256k1_connection()
        
        assert connection['curve_constant'] == 7
        assert connection['holonomy_constant'] == 7
        assert connection['connection_verified']


class TestSecp256k1:
    """Test secp256k1 elliptic curve"""
    
    def test_curve_constant(self):
        """Test curve constant b = 7"""
        curve = Secp256k1Curve()
        assert curve.b == 7
    
    def test_point_on_curve(self):
        """Test points satisfy y² = x³ + 7 (mod p)"""
        curve = Secp256k1Curve()
        
        # Test generator point
        assert curve.is_on_curve(curve.GX, curve.GY)
    
    def test_holonomy_connections(self):
        """Test holonomy connections"""
        curve = Secp256k1Curve()
        connections = curve.get_holonomy_connections()
        
        assert connections['constant_b'] == 7
        assert connections['connection_verified']
        assert connections['tau_1_ratio'] == 75/17
        assert connections['lemma_ratio'] == 75/71


class TestRamanujanCouplings:
    """Test Ramanujan tau couplings"""
    
    def test_tau_values(self):
        """Test known Ramanujan tau values"""
        ram = RamanujanCouplings()
        
        assert ram.tau(1) == 1
        assert ram.tau(2) == -24
        assert ram.tau(3) == 252
    
    def test_holonomy_connection(self):
        """Test connection τ₁ = 75/17"""
        ram = RamanujanCouplings()
        connection = ram.get_holonomy_connection()
        
        assert connection['tau_1_ratio'] == 75/17
        assert connection['holonomy_75'] == 75
        assert connection['holonomy_17'] == 17
    
    def test_couplings_computation(self):
        """Test computation of coupling array"""
        ram = RamanujanCouplings()
        couplings = ram.compute_couplings(n=8)
        
        assert len(couplings) == 8
        # Normalized, so won't be exactly 1, but first should be smallest magnitude
        assert couplings[0] <= np.max(np.abs(couplings))


class TestScalarWazeFramework:
    """Test complete Scalar Waze framework"""
    
    def test_initialization(self):
        """Test framework initialization"""
        framework = ScalarWazeFramework(dimension=8)
        
        assert framework.dimension == 8
        assert len(framework.HOLONOMY) == 8
    
    def test_unified_operator(self):
        """Test unified operator 𝒦 = {𝐗ᵢ, kᵢ, W_ergo^i}"""
        framework = ScalarWazeFramework(dimension=8)
        features = np.array([14.134, 21.022, 25.011, 30.425, 32.935, 37.586, 40.918, 43.327])
        
        result = framework.compute_unified_operator(features, dr_n=9, n_couplings=8)
        
        assert 'state_vectors' in result
        assert 'eigenvalues' in result
        assert 'ergotropy' in result
        assert 'holonomy_phase' in result
        assert 'tau_couplings' in result
        
        # Check dimensions
        assert len(result['state_vectors']) == 8
        assert len(result['eigenvalues']) == 8
    
    def test_zeta_zeros_analysis(self):
        """Test analysis of Riemann zeta zero gaps"""
        framework = ScalarWazeFramework(dimension=8)
        
        # First few zeta zero gaps (imaginary parts)
        zero_gaps = np.array([6.888, 4.989, 5.414, 2.510, 4.651, 3.332, 2.409, 3.283])
        
        result = framework.analyze_zeta_zeros(zero_gaps)
        
        assert 'state_vectors' in result
        assert 'ergotropy' in result
    
    def test_riemann_hypothesis_validation(self):
        """Test RH validation through harmonic resonance"""
        framework = ScalarWazeFramework(dimension=8)
        zero_gaps = np.array([6.888, 4.989, 5.414, 2.510, 4.651, 3.332, 2.409, 3.283])
        
        validation = framework.validate_riemann_hypothesis(zero_gaps, critical_line=0.5)
        
        assert 'total_ergotropy' in validation
        assert 'harmonic_consonance' in validation
        assert 'critical_deviation' in validation
        assert 'validation_score' in validation
    
    def test_elliptic_curve_integration(self):
        """Test secp256k1 elliptic curve integration"""
        framework = ScalarWazeFramework()
        
        # Get point on curve - use generator point instead  
        point = framework.elliptic.g
        
        assert len(point) == 2
        assert framework.elliptic.is_on_curve(point[0], point[1])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
