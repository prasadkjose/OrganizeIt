""" setup.py """

from setuptools import setup

setup(
    name="OrganizeIt",
    version="0.1.0",
    packages=["organize_it"],
    setup_requires=["setuptools-yaml", "jsonschema", "pylint", "GPT4All"],
    install_requires=["setuptools-yaml", "jsonschema", "GPT4All"],
    entry_points={"console_scripts": ["oIt = organize_it.__main__:main"]},
)
