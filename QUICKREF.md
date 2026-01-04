# Scalar Waze Quick Reference

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

```python
from scalar_waze import ScalarWazeFramework
import numpy as np

# Initialize
fw = ScalarWazeFramework(dimension=8)

# Analyze zeta zeros
gaps = np.array([6.888, 4.989, 5.414, 2.510, 4.651, 3.332, 2.409, 3.283])
result = fw.analyze_zeta_zeros(gaps)

# Validate RH
validation = fw.validate_riemann_hypothesis(gaps)
```

## Key Components

### Discrete Rotation

```python
from scalar_waze.discrete_rotation import DiscreteRotationOperator

dr = DiscreteRotationOperator(modulus=9)
value = dr.apply(np.exp(1j * np.pi))  # Returns 8
inv = dr.inverse_element(17)  # Returns 8
```

### Wave Operator

```python
from scalar_waze import ContinuousWaveOperator

wave = ContinuousWaveOperator(modulus=9)
transformed = wave.apply(features, holonomy_phase=0.0)
```

### Quantum System

```python
from scalar_waze import QuantumStateSystem

quantum = QuantumStateSystem(dimension=8)
states = quantum.initialize_states(features)
eigenvalues = quantum.compute_eigenvalues(states)
ergotropy = quantum.compute_ergotropy(states, eigenvalues)
```

### Holonomy

```python
from scalar_waze import HolonomyCalculator

holonomy = HolonomyCalculator()
phase = holonomy.compute_holonomy_phase(dr_n=9)
```

### Elliptic Curve

```python
from scalar_waze.elliptic import Secp256k1Curve

curve = Secp256k1Curve()
is_valid = curve.is_on_curve(x, y)
```

### Ramanujan

```python
from scalar_waze import RamanujanCouplings

ram = RamanujanCouplings()
tau_n = ram.tau(n)
couplings = ram.compute_couplings(n=8)
```

## Important Constants

- **Holonomy Sequence:** `[7, 17, 18, 71, 75, 126, 1275, 4412]`
- **Density Matrix:** `[1/9, 6/9, 2/9]`
- **τ₁ Ratio:** `75/17 = 4.4118`
- **Lemma Ratio:** `75/71 = 1.0563`
- **Curve Constant:** `b = 7`

## Key Formulas

### Master Equation
```
𝒦 = {𝐗ᵢ, kᵢ, W_ergo^i} = Ω̂[{Fᵢ}ᵢ₌₁ᵐ | dr_n, {τₖ}ₖ₌₀ⁿ⁻¹]
```

### Discrete Rotation
```
dr_9(e^(iπ)) = 8 = [17^(-1)]_9
```

### Wave Operator
```
Ω̂[f](s) = ∫_ℂ K_Möbius(s,s') f(s') e^(iφ_dr(s')) ds'
```

### Ergotropy Perturbation
```
δW = (75/71)·sin(Φ/10.414)·1.596·0.498
```

### Elliptic Curve
```
y² = x³ + 7 (mod p)
```

## Testing

```bash
# Run all tests
pytest code/tests/test_scalar_waze.py -v

# Run specific test class
pytest code/tests/test_scalar_waze.py::TestQuantumErgotropy -v

# Run with coverage
pytest code/tests/test_scalar_waze.py --cov=scalar_waze
```

## Examples

```bash
# Analyze zeta zeros
python code/examples/analyze_zeta_zeros.py
```

## Common Tasks

### Validate Riemann Hypothesis
```python
validation = framework.validate_riemann_hypothesis(zero_gaps)
print(f"On critical line: {validation['critical_deviation'] < 0.01}")
print(f"Ergotropy: {validation['total_ergotropy']}")
```

### Compute Holonomy Connections
```python
connections = framework.elliptic.get_holonomy_connections()
print(connections)
```

### Verify Discrete Rotation Properties
```python
dr = framework.dr_operator
print(f"dr_9(e^(iπ)) = {dr.apply(np.exp(1j * np.pi))}")
print(f"[17^(-1)]_9 = {dr.inverse_element(17)}")
print(f"τ₁ = {dr.tau_1_ratio}")
```

## Troubleshooting

### Import Errors
```bash
pip install -e .
```

### Test Failures
```bash
pip install pytest
pytest code/tests/test_scalar_waze.py -v
```

### Numerical Issues
- Check feature normalization
- Verify dimensions match
- Ensure positive definite matrices

## Resources

- **README.md:** User guide
- **ARCHITECTURE.md:** Technical details
- **CONTRIBUTING.md:** Developer guide
- **GitHub:** https://github.com/Holedozer1229/Scalar-Waze

## Contact

- **Author:** Travis Dale Jones
- **Email:** travis.jones@holedozer1229.org
- **GitHub:** @Holedozer1229
