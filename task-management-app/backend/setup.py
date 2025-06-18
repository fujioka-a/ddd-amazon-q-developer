from setuptools import setup, find_packages

setup(
    name="task-management-app",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.13",
    install_requires=[
        "boto3>=1.34.0",
        "PyJWT>=2.8.0",
        "cryptography>=42.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "moto>=4.2.0",
            "black>=23.7.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
        ],
    },
)
