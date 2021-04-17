[![Build status](https://github.com/bincrafters/bincrafters-package-tools/workflows/bincrafters-package-tools/badge.svg)](https://github.com/bincrafters/bincrafters-package-tools/actions)
[![Codecov](https://codecov.io/gh/bincrafters/bincrafters-package-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-package-tools)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-package-tools)

# Bincrafters Package Tools

## A modular toolset for [Conan package tools](https://github.com/conan-io/conan-package-tools)

This project contains files used by Conan Package Tools for all kinds of bincrafters builds.

These scripts are used during build process to allow for rapid testing and prototyping at this time.


#### INSTALL
To install by pip is just one step

##### Local
If you want to install by local copy

    pip install .

##### Remote
Or if you want to download our pip package

    pip install bincrafters_package_tools


#### ENVIRONMENT
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

**BINTRAY_REPOSITORY**: Bintray repository name. This variable replaces "public-conan" for **CONAN_UPLOAD**.

#### Repository configuration
Options that are not specific to a single package build can be specified by adding a bincrafters-package-tools.yml file in the root of the recipes repository.

Sample file:

```yaml
---
# Apply conan config install before building packages
conan_configuration_sources:
  - url: https://server.local/common-conan-configuration.zip
    # Optional arguments
    # type: git
    # args:
    #   - -b
    #   - main
    # verify_ssl: false
    # source_folder: foo
    # target_folder: bar
```

##### Testing and Development
To install extra packages required to test

    pip install '.[test]'


#### TESTING
To run all unit test + code coverage, just execute:

    pip install -r bincrafters/requirements_test.txt
    cd tests
    pytest -v --cov=bincrafters


#### LICENSE
[MIT](LICENSE.md)
