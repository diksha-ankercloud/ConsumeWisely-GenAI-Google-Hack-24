from setuptools import find_packages, setup

REEQUIRES_PYTHON = '>=3.9.6'
VERSION = '0.0.0'

REQUIRED = [
    'pymongo==4.7.3',
    'Flask==3.0.3',
    'flask-cors'
]

setup(
    python_requires=REEQUIRES_PYTHON,
    packages=find_packages(exclude=["test"]),
    install_requires=REQUIRED,
    include_package_data=True
)