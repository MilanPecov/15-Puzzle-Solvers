from setuptools import setup, find_packages

setup(
    name='fifteen_puzzle_solvers',
    version='2.0.0',
    author='Milan Pecov',
    author_email='mpecov@yahoo.ca',
    description='Different solvers for the 15 puzzle sliding game',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MilanPecov/15-Puzzle-Solvers',
    packages=find_packages(include=['fifteen_puzzle_solvers', 'fifteen_puzzle_solvers.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require={
        'GUI': ['tkinter'],
    },
    keywords='15-puzzle sliding-game algorithms A* breadth-first search heuristics python path-finding',
    python_requires='>=3.6',
)
