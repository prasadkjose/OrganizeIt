from setuptools import setup

setup(
    name = 'OrganizeIt',
    version = '0.1.0',
    packages = ['organizeIt'],
    setup_requires = ['setuptools-yaml' , 'jsonschema'],
    install_requires = ['setuptools-yaml' , 'jsonschema'],
    entry_points = {
        'console_scripts': [
            'oIt = organizeIt.__main__:main'
        ]
    })