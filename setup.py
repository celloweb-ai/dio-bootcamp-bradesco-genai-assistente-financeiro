"""Setup configuration for Assistente Financeiro Inteligente."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="assistente-financeiro-ia",
    version="1.0.0",
    author="Marcus Vasconcellos",
    author_email="marcus@vasconcellos.net.br",
    description="Assistente Financeiro Inteligente com IA Generativa - DIO Bootcamp Bradesco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celloweb-ai/dio-bootcamp-bradesco-genai-assistente-financeiro",
    project_urls={
        "Bug Tracker": "https://github.com/celloweb-ai/dio-bootcamp-bradesco-genai-assistente-financeiro/issues",
        "Documentation": "https://github.com/celloweb-ai/dio-bootcamp-bradesco-genai-assistente-financeiro/blob/main/README.md",
        "Source Code": "https://github.com/celloweb-ai/dio-bootcamp-bradesco-genai-assistente-financeiro",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
    },
    entry_points={
        "console_scripts": [
            "assistente-financeiro=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)