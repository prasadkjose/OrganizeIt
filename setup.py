from setuptools import setup

setup(
    name = 'OrganizeIt',
    version = '0.1.0',
    packages = ['organizeIt'],
    entry_points = {
        'console_scripts': [
            'oIt = organizeIt.__main__:main'
        ]
    })