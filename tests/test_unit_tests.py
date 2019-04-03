# -*- coding: utf-8 -*-

import os
import pytest

from bincrafters.build_shared import get_recipe_path


@pytest.fixture()
def set_conanfile_path():
    os.environ["CONAN_CONANFILE"] = "foobar.py"
    yield
    del os.environ["CONAN_CONANFILE"]


def test_get_recipe_path_default():
    assert "conanfile.py" == get_recipe_path()


def test_get_recipe_path_conanfile(set_conanfile_path):
    assert "foobar.py" == get_recipe_path()


def test_get_recipe_path_custom():
    assert os.path.join("tmp", "conanfile.py") == get_recipe_path(cwd="tmp")
