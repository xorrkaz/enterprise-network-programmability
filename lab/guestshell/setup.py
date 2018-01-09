from setuptools import setup, find_packages

setup(
    name='dna-scripts',
    version='0.1',
    packages=find_packages(),
    license='All rights reserved',
    long_description=open('README.md').read(),
    author='Dmitry Figol, Cisco Systems',
    python_requires='==2.7.*',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'outputs_collector = dna.scripts.outputs_collector:main',
        ],
    }
)
