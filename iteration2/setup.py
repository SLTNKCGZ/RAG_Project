from setuptools import setup, find_packages

setup(
    name="cse3063f25grp1",
    version="1.0.0",
    description="RAG System - Iteration 1",
    author="Grp 1",
    author_email="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "mypy>=1.0.0",
        ]
    }
)