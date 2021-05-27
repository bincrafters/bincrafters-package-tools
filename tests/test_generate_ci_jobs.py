# -*- coding: utf-8 -*-

import os
import pytest
from cpt.tools import split_colon_env
from bincrafters.generate_ci_jobs import _generate_gcc_matrices

complete_gcc_matrix = {}
complete_gcc_matrix["config"] = []
complete_gcc_matrix["config"].extend([
    {'name': 'GCC 4.9 x86', 'compiler': 'GCC', 'version': '4.9', 'os': 'ubuntu-18.04', 'arch': 'x86'},
    {'name': 'GCC 4.9 x86_64', 'compiler': 'GCC', 'version': '4.9', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 4.9 armv7', 'compiler': 'GCC', 'version': '4.9', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 4.9 armv7hf', 'compiler': 'GCC', 'version': '4.9', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 5 x86', 'compiler': 'GCC', 'version': '5', 'os': 'ubuntu-18.04', 'arch': 'x86'},
    {'name': 'GCC 5 x86_64', 'compiler': 'GCC', 'version': '5', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 5 armv7', 'compiler': 'GCC', 'version': '5', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 5 armv7hf', 'compiler': 'GCC', 'version': '5', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 5 armv8', 'compiler': 'GCC', 'version': '5', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 6 x86', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'x86'},
    {'name': 'GCC 6 x86_64', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 6 armv7', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 6 armv7hf', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 6 armv8', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 7 x86', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'x86'},
    {'name': 'GCC 7 x86_64', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 7 armv7', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 7 armv7hf', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 7 armv8', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 8 x86', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'x86'},
    {'name': 'GCC 8 x86_64', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 8 armv7', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 8 armv7hf', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 8 armv8', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 9 x86', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'x86'},
    {'name': 'GCC 9 x86_64', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 9 armv7', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 9 armv7hf', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 9 armv8', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 10 x86_64', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 10 armv7', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
    {'name': 'GCC 10 armv7hf', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'}
])

partial_gcc_matrix = {}
partial_gcc_matrix["config"] = []
partial_gcc_matrix["config"].extend([
    {'name': 'GCC 6 x86_64', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 6 armv7hf', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 6 armv8', 'compiler': 'GCC', 'version': '6', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 7 x86_64', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 7 armv7hf', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 7 armv8', 'compiler': 'GCC', 'version': '7', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 8 x86_64', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 8 armv7hf', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 8 armv8', 'compiler': 'GCC', 'version': '8', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 9 x86_64', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 9 armv7hf', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 9 armv8', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 10 x86_64', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 10 armv7hf', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'}
])

complete_clang_matrix = {}
complete_clang_matrix["config"] = []
complete_clang_matrix["config"].extend([
    {"name": "CLANG 3.9 x86", "compiler": "CLANG",
        "version": '3.9', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 3.9 x86_64", "compiler": "CLANG",
        "version": '3.9', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 4.0 x86", "compiler": "CLANG",
        "version": '4.0', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 4.0 x86_64", "compiler": "CLANG",
        "version": '4.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 5.0 x86", "compiler": "CLANG",
        "version": '5.0', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 5.0 x86_64", "compiler": "CLANG",
        "version": '5.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 6.0 x86", "compiler": "CLANG",
        "version": '6.0', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 6.0 x86_64", "compiler": "CLANG",
        "version": '6.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 7.0 x86", "compiler": "CLANG",
        "version": '7.0', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 7.0 x86_64", "compiler": "CLANG",
        "version": '7.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 8 x86", "compiler": "CLANG",
        "version": '8', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 8 x86_64", "compiler": "CLANG",
        "version": '8', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 9 x86", "compiler": "CLANG",
        "version": '9', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 9 x86_64", "compiler": "CLANG",
        "version": '9', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 10 x86", "compiler": "CLANG",
        "version": '10', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 10 x86_64", "compiler": "CLANG",
        "version": '10', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 11 x86", "compiler": "CLANG",
        "version": '11', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 11 x86_64", "compiler": "CLANG",
        "version": '11', "os": "ubuntu-18.04", "arch": "x86_64"},
])


@pytest.fixture()
def set_all_bpt_conan_archs():
    os.environ["BPT_CONAN_ARCHS"] = "x86, x86_64, armv7, armv7hf, armv8"
    yield
    del os.environ["BPT_CONAN_ARCHS"]

@pytest.fixture()
def set_all_bpt_gcc_versions():
    os.environ["BPT_GCC_VERSIONS"] = "4.9,5,6,7,8,9,10"
    yield
    del os.environ["BPT_GCC_VERSIONS"]

@pytest.fixture()
def set_all_bpt_clang_versions():
    os.environ["BPT_CLANG_VERSIONS"] = ["3.9","4.0","4.9","5","6","7","8","9","10"]
    yield
    del os.environ["BPT_CLANG_VERSIONS"]

@pytest.fixture()
def set_partial_bpt_conan_archs():
    os.environ["BPT_CONAN_ARCHS"] = "x86_64, armv7hf, armv8"
    yield
    del os.environ["BPT_CONAN_ARCHS"]

@pytest.fixture()
def set_partial_bpt_gcc_versions():
    os.environ["BPT_GCC_VERSIONS"] = "6,7,8,9,10"
    yield
    del os.environ["BPT_GCC_VERSIONS"]

@pytest.fixture()
def set_partial_bpt_clang_versions():
    os.environ["BPT_CLANG_VERSIONS"] = ["8","9","10"]
    yield
    del os.environ["BPT_CLANG_VERSIONS"]

def test_generate_complete_gcc_matrix(set_all_bpt_conan_archs, set_all_bpt_gcc_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []

    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_GCC_VERSIONS")
    # Act
    matrix["config"]  = _generate_gcc_matrices(compiler_archs,compiler_versions)
    # Assert
    assert matrix["config"] == complete_gcc_matrix["config"]

def test_generate_partial_gcc_matrix(set_partial_bpt_conan_archs, set_partial_bpt_gcc_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []

    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_GCC_VERSIONS")
    # Act
    matrix["config"]  = _generate_gcc_matrices(compiler_archs,compiler_versions)

    # Assert
    assert matrix["config"] == partial_gcc_matrix["config"]

# def test_generate_gcc_matrix():
#     # Arrange
#     matrix =  {}
#     matrix["config"] = []
#     # Act
#     matrix["config"].extend(
#         _generate_clang_matrix(valid_clang_archs, "3.9", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "4.0", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "5.0", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "6.0", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "7.0", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "8", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "9", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "10", ["x86","x86_64"]) +
#         _generate_clang_matrix(valid_clang_archs, "11", ["x86","x86_64"])
#     )
#     print(matrix["config"])
#     print("\n", valid_clang_matrix["config"])
#     # Assert
#     assert matrix["config"] == valid_clang_matrix["config"]
