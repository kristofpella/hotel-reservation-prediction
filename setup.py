from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='project-hotel-reservation',
    version='0.1',
    author='Kristof Pella',
    packages=find_packages(),
    install_requires=requirements,
)