import os
import pathlib

from setuptools import setup, find_packages

v_default = "0.0.1"
v_env = os.getenv("v")
v = v_env if v_env else v_default

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "docs" / "README.md").read_text()

setup(
    name="link-scape",
    version=v,
    description="Python library to plot force-directed graphs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aloneguid/linkscape",
    author="Ivan Gavryliuk",
    author_email="ifs5vh19k@mozmail.com",
    license="Apache-2.0",
    packages=find_packages(),
    include_package_data=True
)

# 1. run python setup.py bdist_wheel
# 2. twine upload dist/*

# https://realpython.com/pypi-publish-python-package/#adding-files-to-your-package