from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scalar-waze",
    version="1.0.0",
    author="Travis Dale Jones",
    author_email="travis.jones@holedozer1229.org",
    description="A Transcendent Unification of Number Theory, Quantum Mechanics, Geometry, and Musical Harmony",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Holedozer1229/Scalar-Waze",
    packages=find_packages(where="code"),
    package_dir={"": "code"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "mpmath>=1.2.0",
        "sympy>=1.9",
    ],
    extras_require={
        "dev": ["pytest>=6.2.0", "jupyter>=1.0.0"],
    },
)
