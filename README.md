[![Build Status](https://travis-ci.org/bincrafters/bincrafters-package-tools.svg?branch=master)](https://travis-ci.org/bincrafters/bincrafters-package-tools)
[![codecov](https://codecov.io/gh/bincrafters/bincrafters-package-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-package-tools)

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


#### TESTING
To run all unit test + code coverage, just execute:

    cd bincrafters/test
    pytest -v --cov=bincrafters


#### LICENSE
[MIT](LICENSE.md)
