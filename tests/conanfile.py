from conans import ConanFile
from conans import tools


class FoobarConan(ConanFile):
    name = "foobar"
    version = "0.1.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "<Description of Foobar here>"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "None"
    license = "None"

    def package(self):
        self.copy("*")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
