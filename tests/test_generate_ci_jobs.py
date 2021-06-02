# -*- coding: utf-8 -*-
from bincrafters.generate_mac_jobs import generate_mac_matrices
import os
import pytest

from bincrafters.generate_win_jobs import generate_win_matrices
from bincrafters.generate_clang_jobs import generate_clang_matrices
from bincrafters.generate_gcc_jobs import generate_gcc_matrices
from cpt.tools import split_colon_env

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
    {'name': 'GCC 9 x86_64', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 9 armv7hf', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'},
    {'name': 'GCC 9 armv8', 'compiler': 'GCC', 'version': '9', 'os': 'ubuntu-18.04', 'arch': 'armv8'},
    {'name': 'GCC 10 x86_64', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
    {'name': 'GCC 10 armv7hf', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'}
])

complete_clang_matrix = {}
complete_clang_matrix["config"] = []
complete_clang_matrix["config"].extend([
    {"name": "CLANG 3.9 x86_64", "compiler": "CLANG","version": '3.9', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 4.0 x86_64", "compiler": "CLANG","version": '4.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 5.0 x86_64", "compiler": "CLANG","version": '5.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 6.0 x86_64", "compiler": "CLANG","version": '6.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 7.0 x86", "compiler": "CLANG","version": '7.0', "os": "ubuntu-18.04", "arch": "x86"},
    {"name": "CLANG 7.0 x86_64", "compiler": "CLANG","version": '7.0', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 8 x86_64", "compiler": "CLANG","version": '8', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 9 x86_64", "compiler": "CLANG","version": '9', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 10 x86_64", "compiler": "CLANG","version": '10', "os": "ubuntu-18.04", "arch": "x86_64"},
    {"name": "CLANG 11 x86_64", "compiler": "CLANG","version": '11', "os": "ubuntu-18.04", "arch": "x86_64"},
])

complete_mac_matrix = {}
complete_mac_matrix["config"] = []
complete_mac_matrix["config"].extend([
    {"name": "macOS Apple-Clang 10", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.15"},
    {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
    {"name": "macOS Apple-Clang 12", "compiler": "APPLE_CLANG", "version": "12.0", "os": "macOS-10.15"},
])

complete_win_matrix = {}
complete_win_matrix["config"] = []
complete_win_matrix["config"].extend([
    {"name": "Windows VS 2017 x86", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "arch": "x86"}, 
    {"name": "Windows VS 2017 x86_64", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "arch": "x86_64"}, 
    {"name": "Windows VS 2017 armv7", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "arch": "armv7"}, 
    {"name": "Windows VS 2019 x86", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "arch": "x86"}, 
    {"name": "Windows VS 2019 x86_64", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "arch": "x86_64"}, 
    {"name": "Windows VS 2019 armv7", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "arch": "armv7"}, 
    {"name": "Windows VS 2019 armv8", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "arch": "armv8"}, 
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
    os.environ["BPT_CLANG_VERSIONS"] = "3.9,4,5,6,7,8,9,10,11"
    yield
    del os.environ["BPT_CLANG_VERSIONS"]

@pytest.fixture()
def set_all_bpt_mac_versions():
    os.environ["BPT_MAC_VERSIONS"] = "10,11,12"
    yield
    del os.environ["BPT_MAC_VERSIONS"]

@pytest.fixture()
def set_all_bpt_win_versions():
    os.environ["BPT_WIN_VERSIONS"] = "2017, 2019"
    yield
    del os.environ["BPT_WIN_VERSIONS"]

@pytest.fixture()
def set_partial_bpt_conan_archs():
    os.environ["BPT_CONAN_ARCHS"] = "x86_64, armv7hf, armv8"
    yield
    del os.environ["BPT_CONAN_ARCHS"]

@pytest.fixture()
def set_partial_bpt_gcc_versions():
    os.environ["BPT_GCC_VERSIONS"] = "6,7,9,10"
    yield
    del os.environ["BPT_GCC_VERSIONS"]

@pytest.fixture()
def set_partial_bpt_clang_versions():
    os.environ["BPT_CLANG_VERSIONS"] = "8,9,10"
    yield
    del os.environ["BPT_CLANG_VERSIONS"]

@pytest.fixture()
def set_partial_bpt_mac_versions():
    os.environ["BPT_MAC_VERSIONS"] = "11,12"
    yield
    del os.environ["BPT_MAC_VERSIONS"]

@pytest.fixture()
def set_partial_bpt_win_versions():
    os.environ["BPT_WIN_VERSIONS"] = "2019"
    yield
    del os.environ["BPT_WIN_VERSIONS"]

def test_generate_complete_gcc_matrix(set_all_bpt_conan_archs, set_all_bpt_gcc_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []
    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_GCC_VERSIONS")
    # Act
    matrix["config"]  = generate_gcc_matrices(compiler_archs, compiler_versions)
    # Assert
    assert matrix["config"] == complete_gcc_matrix["config"]

def test_generate_partial_gcc_matrix(set_partial_bpt_conan_archs, set_partial_bpt_gcc_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []
    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_GCC_VERSIONS")
    # Act
    matrix["config"] = generate_gcc_matrices(compiler_archs, compiler_versions)
    # Assert
    assert matrix["config"] == partial_gcc_matrix["config"]

def test_generate_complete_clang_matrix(set_all_bpt_conan_archs, set_all_bpt_clang_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []
    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_CLANG_VERSIONS")
    # Act
    matrix["config"] = generate_clang_matrices(compiler_archs, compiler_versions)
    # Assert
    assert matrix["config"] == complete_clang_matrix["config"]

def test_generate_complete_win_matrix(set_all_bpt_conan_archs, set_all_bpt_win_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []
    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_WIN_VERSIONS")
    # Act
    matrix["config"] = generate_win_matrices(compiler_archs, compiler_versions)
    print(matrix["config"])
    print()
    print(complete_win_matrix["config"])
    # Assert
    assert matrix["config"] == complete_win_matrix["config"]

def test_generate_complete_win_matrix(set_all_bpt_conan_archs, set_all_bpt_mac_versions,):
    # Arrange
    matrix =  {}
    matrix["config"] = []
    compiler_archs = split_colon_env("BPT_CONAN_ARCHS")
    compiler_versions = split_colon_env("BPT_MAC_VERSIONS")
    # Act
    matrix["config"] = generate_mac_matrices(compiler_archs, compiler_versions)
    print(matrix["config"])
    print()
    print(complete_mac_matrix["config"])
    # Assert
    assert matrix["config"] == complete_mac_matrix["config"]