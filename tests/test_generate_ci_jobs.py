# -*- coding: utf-8 -*-

from bincrafters.generate_ci_jobs import _generate_gcc_matrix
import os
import pytest

valid_gcc_archs = ["x86", "x86_64", "armv7", "armv7hf", "armv8"]
valid_gcc_versions = ["4.9", "5", "6", "7", "8", "9", "10"]
valid_gcc_matrix = {}
valid_gcc_matrix["config"] = [
    {'name': 'GCC 4.9 x86', 'compiler': 'GCC', 'version': '4.9', 'os': 'ubuntu-18.04', 'arch': 'x86'},
        {'name': 'GCC 4.9 x86_64', 'compiler': 'GCC', 'version': '4.9', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
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
        {'name': 'GCC 10 x86', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'x86'},
        {'name': 'GCC 10 x86_64', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'x86_64'},
        {'name': 'GCC 10 armv7', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'armv7'},
        {'name': 'GCC 10 armv7hf', 'compiler': 'GCC', 'version': '10', 'os': 'ubuntu-18.04', 'arch': 'armv7hf'}
]

def test_generate_gcc_matrix():
    assert valid_gcc_matrix == _generate_gcc_matrix(valid_gcc_archs, valid_gcc_versions)