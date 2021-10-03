[![Build status](https://github.com/bincrafters/bincrafters-package-tools/workflows/bincrafters-package-tools/badge.svg)](https://github.com/bincrafters/bincrafters-package-tools/actions)
[![Codecov](https://codecov.io/gh/bincrafters/bincrafters-package-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-package-tools)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-package-tools)

# Bincrafters Package Tools

## A modular toolset for [Conan Package Tools](https://github.com/conan-io/conan-package-tools)

This project contains files used by Conan Package Tools for all kinds of bincrafters builds.

These scripts are used during build process to allow for rapid testing and prototyping at this time.


### INSTALL
To install by pip is just one step

### Local
If you want to install by local copy

    pip install .

### Remote
Or if you want to download our pip package

    pip install bincrafters_package_tools


### ENVIRONMENT VARIABLES
All variables supported by Conan package tools, are treated by Bincrafters package tools as well.
To solve the upload, some variables are customized by default:

**CONAN_UPLOAD**: https://bincrafters.jfrog.io/artifactory/api/conan/public-conan  
**CONAN_REFERENCE**: Fields **name** and **version** from conanfile.py  
**CONAN_USERNAME**: Get from CI env vars. Otherwise, use **bincrafters**  
**CONAN_VERSION**: Get from CI env vars.  
**CONAN_VERSION**: Field **version** from conanfile.py  
**CONAN_UPLOAD_ONLY_WHEN_STABLE**: True for default template. False for Boost builds.  
**CONAN_STABLE_BRANCH_PATTERN**: stable/\*  
**CONAN_ARCHS**: Only x86_64 per default. To build 32-bit and 64-bit use e.g. [x86_64, x86]

___

**BPT SPECIFIC ENVIRONMENT VARIBLES**:

**BPT_MATRIX_SPLIT_BY_BUILD_TYPES**: Splits build jobs into `Release` and `Debug` build jobs.
**BPT_MATRIX_DISCARD_DUPLICATE_BUILD_IDS**: `true`/`false`, default: `true`. This does NOT YET what it says. Right now, this only has an effect for installer_only and header_only recipes when set to `false`. In those cases, you get the full build matrix, instead of a shortened build matrix. In the future, the matrix generation actually compares build IDs and discards jobs based on the IDs.

___


#### Testing and Development
To install extra packages required to test

    pip install .[test]


#### TESTING
To run all unit test + code coverage, just execute:

    pip install -r bincrafters/requirements_test.txt
    cd tests
    pytest -v --cov=bincrafters


#### LICENSE
[MIT](LICENSE.md)
