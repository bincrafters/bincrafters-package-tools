# -*- coding: utf-8 -*-

import tempfile
import contextlib
import os
from bincrafters import build_shared


recipe_with_shared_1 = """
class FoobarConan(ConanFile):
    name = "foobar"
    version = "0.1.0"
    url = "https://github.com/bincrafters/foobar"
    description = "Just another foobar "
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"with_zlib": [True, False],
               "build_tests": [True, False],
               "build_binaries": [True, False],
               "static_rt": [True, False],
               "shared": [True, False],  # Just another comment
               }
    default_options = "with_zlib=False", "build_tests=False", "static_rt=True", "build_binaries=True", "shared=False"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def requirements(self):
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")

    def source(self):
        repo_url = "https://github.com/bincrafters/foobar.git"
        self.run("git clone -b v{0} {1} {2}".format(self.version, repo_url, self.source_subfolder))

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
"""

recipe_with_shared_2 = """
class FoobarConan(ConanFile):
    name="foobar"
    version="0.1.0"
    url="https://github.com/bincrafters/foobar"
    description="Just another foobar "
    license="MIT"
    exports="LICENSE.md"
    exports_sources="CMakeLists.txt"
    generators="cmake"
    settings="os", "arch", "compiler", "build_type"
    options={"shared": [True, False]}
    default_options="shared=False"

    def source(self):
        repo_url = "https://github.com/bincrafters/foobar.git"
        self.run("git clone -b v{0} {1} {2}".format(self.version, repo_url, self.source_subfolder))

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
"""

recipe_with_no_shared_1 = """
    name = "foobar"
    version = "0.1.0"
    no_copy_source = True

    def source(self):
        self.run("git clone ...")
        tools.download("url", "file.zip")
        tools.unzip("file.zip" )

    def package(self):
        self.copy("*.h", "include")


    def package_id(self):
        self.info.header_only()
"""

recipe_with_no_shared_2 = """
class FoobarConan(ConanFile):
    name = "foobar"
    version = "0.1.0"
    url = "https://github.com/bincrafters/foobar"
    description = "Just another foobar "
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"with_zlib": [True, False],
               "build_tests": [True, False],
               "build_binaries": [True, False],
               "static_rt": [True, False]
               }
    default_options = "with_zlib=False", "build_tests=False", "static_rt=True", "build_binaries=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def requirements(self):
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")

    def source(self):
        repo_url = "https://github.com/bincrafters/foobar.git"
        self.run("git clone -b v{0} {1} {2}".format(self.version, repo_url, self.source_subfolder))

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
"""


@contextlib.contextmanager
def chdir(path):
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def create_and_validate(recipe_buffer, expected_value):
    tempdir = tempfile.mkdtemp()
    with chdir(tempdir):
        with open("conanfile.py", "w") as fd:
            fd.write(recipe_buffer)
            fd.flush()
            assert expected_value == build_shared.is_shared()


def test_recipe_with_shared_option():
    create_and_validate(recipe_with_shared_1, True)
    create_and_validate(recipe_with_shared_2, True)


def test_recipe_with_no_shared_option():
    create_and_validate(recipe_with_no_shared_1, False)
    create_and_validate(recipe_with_no_shared_2, False)
