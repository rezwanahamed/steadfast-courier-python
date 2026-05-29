"""
Setup configuration for SteadFast Courier Python package.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="steadfast-courier",
    version="1.0.0",
    author="Rezwan Ahamed",
    author_email="rezwan@example.com",
    description="Professional Python package for SteadFast Courier API integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rezwanahamed/steadfast-courier-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Framework :: FastAPI",
        "Framework :: Flask",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="steadfast courier api shipping logistics delivery",
    project_urls={
        "Bug Reports": "https://github.com/rezwanahamed/steadfast-courier-python/issues",
        "Source": "https://github.com/rezwanahamed/steadfast-courier-python",
        "Documentation": "https://github.com/rezwanahamed/steadfast-courier-python/blob/main/README.md",
        "Author": "https://github.com/rezwanahamed",
    },
)
