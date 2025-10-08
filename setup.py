from setuptools import setup, find_packages

setup(
    name="paraconsistent-toolchain",
    version="0.1.0",
    packages=find_packages(include=["toolchain*", "utils*"]),
    description="A toolchain for exploring paraconsistent development methodologies.",
    author="Jules, AI Agent",
    install_requires=[
        "flake8",
        "bandit",
        "black",
    ],
    python_requires=">=3.9",
)
