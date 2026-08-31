from setuptools import setup, find_packages

setup(
    name="pipecraft-engine",
    version="2.5.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "prometheus-client>=0.17.0",
        "httpx>=0.24.0"
    ],
    entry_points={
        "console_scripts": [
            "pipecraft=api.cli:main",
        ],
    },
)
