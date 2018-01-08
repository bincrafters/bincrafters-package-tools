[![Build Status](https://travis-ci.org/bincrafters/bincrafters-package-tools.svg?branch=master)](https://travis-ci.org/bincrafters/bincrafters-package-tools)
[![codecov](https://codecov.io/gh/bincrafters/bincrafters-package-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-package-tools)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-package-tools)

# Bincrafters Package Tools

## A modular toolset for Conan package tools

This project contains files used by Conan Package Tools for all kinds of bincrafters builds.

These scripts are used during build process to allow for rapid testing and prototyping at this time.


#### INSTALL
To install by pip is just one step

##### Local
If you want to install by local copy

    pip install .

##### Remote
Or if you want to download our pip package

    pip install bincrafters-package-tools

##### Testing and Development
To install extra packages required to test

    pip install .[test]


#### TESTING
To run all unit test + code coverage, just execute:

    pip install -r bincrafters/requirements_test.txt
    cd tests
    pytest -v --cov=bincrafters


#### REQUIREMENTS and DEVELOPMENT
To develop or run Bincrafters package tools, Conan package tools will be required
However, you could solve by pip

    pip install -r bincrafters/requirements.txt


#### UPLOAD
To upload this package on pypi (legacy mode):

    pip install twine
    python setup.py sdist
    twine upload dist/*


#### LICENSE
[MIT](LICENSE.md)
