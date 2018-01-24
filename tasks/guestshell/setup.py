from setuptools import setup, find_packages
from setuptools.command.install import install
from pkgutil import find_loader


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        if find_loader('cli'):
            import dna
            dna.scripts.config_diff.save_config_to_ios_file(override=False)


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
            'config_diff_to_spark = dna.scripts.config_diff:main',
            'record_commands = dna.scripts.record_commands:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
