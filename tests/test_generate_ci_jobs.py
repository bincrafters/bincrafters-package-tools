# -*- coding: utf-8 -*-

from bincrafters.generate_ci_jobs import _generate_gcc_matrix, _generate_clang_matrix
import os
import pytest

valid_gcc_archs = ["x86", "x86_64", "armv7", "armv7hf", "armv8"]
valid_gcc_versions = ["4.9", "5", "6", "7", "8", "9", "10"]
valid_clang_archs = ["x86", "x86_64"]
valid_clang_versions = ["3.9","4.0","5.0","6.0","7.0","8","9","10","11"]

valid_gcc_matrix = {}
valid_gcc_matrix["config"] = []
valid_gcc_matrix["config"].extend([
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

valid_clang_matrix = {}
valid_clang_matrix["config"] = []
valid_clang_matrix["config"].extend([
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

def test_generate_gcc_matrix():
    # Arrange
    matrix =  {}
    matrix["config"] = []
    # Act
    matrix["config"].extend(
        _generate_gcc_matrix(valid_gcc_archs, "4.9", ["x86", "x86_64", "armv7", "armv7hf"]) +
        _generate_gcc_matrix(valid_gcc_archs, "5", ["x86","x86_64","armv7","armv7hf","armv8"]) +
        _generate_gcc_matrix(valid_gcc_archs, "6", ["x86","x86_64","armv7","armv7hf","armv8"]) +
        _generate_gcc_matrix(valid_gcc_archs, "7", ["x86","x86_64","armv7","armv7hf","armv8"]) +
        _generate_gcc_matrix(valid_gcc_archs, "8", ["x86","x86_64","armv7","armv7hf","armv8"]) +
        _generate_gcc_matrix(valid_gcc_archs, "9", ["x86","x86_64","armv7","armv7hf","armv8"]) +
        _generate_gcc_matrix(valid_gcc_archs, "10", ["x86_64","armv7","armv7hf"])
    )
    # Assert
    assert matrix["config"] == valid_gcc_matrix["config"]

def test_generate_gcc_matrix():
    # Arrange
    matrix =  {}
    matrix["config"] = []
    # Act
    matrix["config"].extend(
        _generate_clang_matrix(valid_clang_archs, "3.9", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "4.0", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "5.0", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "6.0", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "7.0", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "8", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "9", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "10", ["x86","x86_64"]) +
        _generate_clang_matrix(valid_clang_archs, "11", ["x86","x86_64"])
    )
    print(matrix["config"])
    print("\n", valid_clang_matrix["config"])
    # Assert
    assert matrix["config"] == valid_clang_matrix["config"]
