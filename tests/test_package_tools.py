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


os.environ["CONAN_GCC_VERSIONS"] = "7"

def _set_upload_when_stable():
    os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = "FOOBAR"

def _get_upload_when_stable():
    return os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"]

def test_build_template_boost_default():
    _set_upload_when_stable()
    builder = build_template_boost_default.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
    assert 8 == len(builder.items)
    assert "" == _get_upload_when_stable()

def test_build_template_boost_default_non_pure_c():
    _set_upload_when_stable()
    builder = build_template_boost_default.get_builder(pure_c=False)
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
    assert 16 == len(builder.items)
    assert "" == _get_upload_when_stable()

def test_build_template_default():
    builder = build_template_default.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
    assert 8 == len(builder.items)

def test_build_template_default_non_pure_c():
    builder = build_template_default.get_builder(pure_c=False)
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
    assert 16 == len(builder.items)

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

def test_build_boost_header_only():
    _set_upload_when_stable()
    builder = build_template_boost_header_only.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert 0 == len(options)
    assert 1 == len(builder.items)
    assert "" == _get_upload_when_stable()

def test_get_os():
    expected_os = platform.system()
    assert expected_os == build_shared.get_os()

def test_ci_is_running():
    expected = True if os.getenv("CI", None) is not None else False
    assert expected == build_shared.is_ci_running()
