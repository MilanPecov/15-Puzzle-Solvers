from setuptools import setup, find_packages

setup(
    author='Milan Pecov',
    description='Different solvers for the 15 puzzle sliding game',
    name='fifteen_puzzle_solvers',
    packages=find_packages(include=['fifteen_puzzle_solvers', 'fifteen_puzzle_solvers.*']),
    version='1.0.3',
)
