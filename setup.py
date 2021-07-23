from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='log-analyzer',
    version='1.1',
    packages=[''],
    url='https://github.com/codemonkey500/cowrie-snort-log-analyzer',
    license='GNU General Public License v3.0',
    author='codemonkey500',
    author_email='kali.linux14@hotmail.com',
    description='Script to analyse cowrie and snort LOG-Data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["pandas>=1.2.4", "SQLAlchemy>=1.4.17", "matplotlib>=3.4.2", "pycountry>=20.7.3", "numpy>=1.20.3",
                      "IP2Location>=8.6.0", "cryptography>=3.4.7", "setuptools>=57.0.0"]
)
