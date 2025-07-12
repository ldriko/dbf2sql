"""
Setup script for DBF to SQL Converter
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="dbf2sql",
    version="1.0.0",
    author="DBF2SQL Team",
    author_email="contact@dbf2sql.com",
    description="A memory-efficient Python tool to convert DBF files to SQL INSERT statements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dbf2sql",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/dbf2sql/issues",
        "Documentation": "https://github.com/yourusername/dbf2sql/blob/main/README.md",
        "Source Code": "https://github.com/yourusername/dbf2sql",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "dbf2sql": ["py.typed", "*.pyi"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "mypy>=1.0",
            "black>=22.0",
            "flake8>=5.0",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dbf2sql=dbf2sql.cli:main",
        ],
    },
    keywords="dbf sql converter database dbase",
    zip_safe=False,
)
