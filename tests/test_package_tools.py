#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_shared
from bincrafters import build_template_boost_default
from bincrafters import build_template_boost_header_only
from bincrafters import build_template_default
from bincrafters import build_template_header_only
from bincrafters import build_template_installer
import os
import platform
import pytest


@pytest.fixture(autouse=True)
def set_matrix_variables():
    if platform.system() == "Linux":
        os.environ["CONAN_GCC_VERSIONS"] = "7"
    elif platform.system() == "Windows":
        os.environ["CONAN_VISUAL_VERSIONS"] = "15"
    elif platform.system() == "Darwin":
        os.environ["CONAN_APPLE_CLANG_VERSIONS"] = "9.0"

@pytest.fixture()
def set_minimal_build_environment():
    os.environ["CONAN_ARCHS"] = "x86"
    os.environ["CONAN_BUILD_TYPES"] = "Release"
    yield
    del os.environ["CONAN_ARCHS"]
    del os.environ["CONAN_BUILD_TYPES"]

@pytest.fixture()
def set_upload_when_stable():
    os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = "FOOBAR"


def get_upload_when_stable():
    return os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"]


def test_build_template_boost_default(set_upload_when_stable):
    builder = build_template_boost_default.get_builder()

    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
        assert "boost_*:shared" in options
        if platform.system() == "Darwin":
            assert "x86_64" == settings['arch']

    if platform.system() == "Linux":
        assert 16 == len(builder.items)
    elif platform.system() == "Windows":
        assert 12 == len(builder.items)
    elif platform.system() == "Darwin":
        assert 4 == len(builder.items)

    assert "" == get_upload_when_stable()


def test_build_template_default():
    builder = build_template_default.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
        if platform.system() == "Darwin":
            assert "x86_64" == settings['arch']

    if platform.system() == "Linux":
        assert 8 == len(builder.items)
    elif platform.system() == "Windows":
        assert 12 == len(builder.items)
    elif platform.system() == "Darwin":
        assert 4 == len(builder.items)

    assert builder.upload_only_when_stable


def test_build_template_default_minimal(set_minimal_build_environment):
    builder = build_template_default.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
        assert "x86" == settings['arch']

    if platform.system() == "Linux":
        assert 2 == len(builder.items)
    elif platform.system() == "Windows":
        assert 3 == len(builder.items)
    elif platform.system() == "Darwin":
        assert 2 == len(builder.items)


def test_build_template_default_non_pure_c():
    builder = build_template_default.get_builder(pure_c=False)
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
        if platform.system() == "Darwin":
            assert "x86_64" == settings['arch']

    if platform.system() == "Linux":
        assert 16 == len(builder.items)
    elif platform.system() == "Windows":
        assert 12 == len(builder.items)
    elif platform.system() == "Darwin":
        assert 4 == len(builder.items)


def test_build_shared():
    builder = build_shared.get_builder()
    assert 0 == len(builder.items)


def test_build_template_installer():
    builder = build_template_installer.get_builder()
    assert 0 == len(builder.items)


def test_build_header_only():
    builder = build_template_header_only.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert 0 == len(options)
    assert 1 == len(builder.items)


def test_build_boost_header_only(set_upload_when_stable):
    builder = build_template_boost_header_only.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert 0 == len(options)
    assert 1 == len(builder.items)
    assert "" == get_upload_when_stable()


def test_get_os():
    expected_os = "Macos" if platform.system() == "Darwin" else platform.system()
    assert expected_os == build_shared.get_os()


def test_ci_is_running():
    expected = True if os.getenv("CI", None) is not None else False
    assert expected == build_shared.is_ci_running()

def test_build_policy_not_set():
    builder = build_template_default.get_builder()
    assert None == builder.build_policy

def test_build_policy_set_in_args():
    builder = build_template_default.get_builder(build_policy='missing')
    assert 'missing' == builder.build_policy

def test_build_policy_set_header_only():
    builder = build_template_header_only.get_builder(build_policy='missing')
    assert 'missing' == builder.build_policy
