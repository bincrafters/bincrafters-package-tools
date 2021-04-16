# -*- coding: utf-8 -*-

import os
import platform
import pytest
from bincrafters.configuration import GlobalConfiguration


def test_default_global_configuration():
    default_configuration = GlobalConfiguration("non_existent_configuration.yml")
    assert len(default_configuration.conan_configuration_sources) == 0


def test_empty_global_configuration():
    empty_configuration = GlobalConfiguration("configuration/empty.yml")
    assert len(empty_configuration.conan_configuration_sources) == 0


def test_conan_configuration_sources():
    cfg = GlobalConfiguration("configuration/conan_configuration_installs.yml")
    assert len(cfg.conan_configuration_sources) == 4
    assert cfg.conan_configuration_sources[0]["url"] == "https://github.com/"


