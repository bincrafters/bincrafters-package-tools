import os
import platform
import pytest
from bincrafters import build_shared
from bincrafters import build_autodetect


@pytest.fixture(autouse=True)
def set_matrix_variables():
    if platform.system() == "Linux":
        os.environ["CONAN_GCC_VERSIONS"] = "7"
    elif platform.system() == "Windows":
        os.environ["CONAN_VISUAL_VERSIONS"] = "15"
    elif platform.system() == "Darwin":
        os.environ["CONAN_APPLE_CLANG_VERSIONS"] = "9.0"


@pytest.fixture()
def set_installer_only_recipe():
    os.environ["CONAN_CONANFILE"] = "conanfile_installer_only.py"
    yield
    del os.environ["CONAN_CONANFILE"]


@pytest.fixture()
def set_header_only_recipe():
    os.environ["CONAN_CONANFILE"] = "conanfile_header_only.py"
    yield
    del os.environ["CONAN_CONANFILE"]


@pytest.fixture()
def set_minimal_build_environment():
    os.environ["CONAN_ARCHS"] = "x86_64"
    os.environ["CONAN_BUILD_TYPES"] = "Release"
    yield
    del os.environ["CONAN_ARCHS"]
    del os.environ["CONAN_BUILD_TYPES"]


@pytest.fixture()
def set_upload_when_stable_false():
    os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = "0"
    yield
    del os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"]


@pytest.fixture()
def set_upload_address():
    os.environ["CONAN_UPLOAD"] = "https://api.bintray.com/conan/foo/bar@False@remotefoo"
    yield
    del os.environ["CONAN_UPLOAD"]


@pytest.fixture()
def set_remote_address():
    os.environ["CONAN_REMOTES"] = "https://api.bintray.com/conan/foo/bar@False@remotefoo"
    yield
    del os.environ["CONAN_REMOTES"]


@pytest.fixture()
def set_multi_remote_address():
    os.environ["CONAN_REMOTES"] = "https://api.bintray.com/conan/foo/bar,https://api.bintray.com/conan/qux/baz"
    yield
    del os.environ["CONAN_REMOTES"]


@pytest.fixture()
def set_mixed_remote_address():
    os.environ["CONAN_REMOTES"] = "https://api.bintray.com/conan/foo/bar@False@remotefoo,https://api.bintray.com/conan/qux/baz"
    yield
    del os.environ["CONAN_REMOTES"]


def test_build_template_default():
    builder = build_autodetect._get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
        if platform.system() == "Darwin":
            assert "x86_64" == settings['arch']

    if platform.system() == "Linux":
        assert 8 == len(builder.items)
    elif platform.system() == "Windows":
        assert 6 == len(builder.items)
    elif platform.system() == "Darwin":
        assert 4 == len(builder.items)

    assert True == builder.upload_only_when_stable


def test_build_template_default_minimal(set_minimal_build_environment):
    builder = build_autodetect._get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert "foobar:shared" in options
        assert "x86_64" == settings['arch']

    if platform.system() == "Linux":
        assert 4 == len(builder.items)
    elif platform.system() == "Windows":
        assert 3 == len(builder.items)
    elif platform.system() == "Darwin":
        assert 2 == len(builder.items)


# TODO: Update test
# def test_build_template_default_non_pure_c():
#     builder = build_autodetect._get_builder(pure_c=False)
#     for settings, options, env_vars, build_requires, reference in builder.items:
#         assert "foobar:shared" in options
#         assert "x86_64" == settings['arch']
#
#     if platform.system() == "Linux":
#         assert 8 == len(builder.items)
#     elif platform.system() == "Windows":
#         assert 6 == len(builder.items)
#     elif platform.system() == "Darwin":
#         assert 4 == len(builder.items)


def test_build_shared():
    builder = build_shared.get_builder()
    assert 0 == len(builder.items)


def test_build_template_installer(set_installer_only_recipe):
    builder = build_autodetect._get_builder()
    assert 1 == len(builder.items)


def test_build_header_only(set_header_only_recipe):
    builder = build_autodetect._get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        assert 0 == len(options)
    assert 1 == len(builder.items)


def test_get_os():
    expected_os = "Macos" if platform.system() == "Darwin" else platform.system()
    assert expected_os == build_shared.get_os()


def test_build_policy_not_set():
    builder = build_autodetect._get_builder()
    assert None == builder.build_policy


def test_upload_only_when_stable_builder(set_upload_when_stable_false):
    builder = build_autodetect._get_builder()
    assert False == builder.upload_only_when_stable


def test_upload_only_when_stable_header_only(set_upload_when_stable_false):
    builder = build_autodetect._get_builder()
    assert False == builder.upload_only_when_stable


def test_format_upload(set_upload_address):
    builder = build_autodetect._get_builder()
    assert "remotefoo" == builder.remotes_manager.upload_remote_name
    assert "remotefoo" == builder.remotes_manager._upload.name
    assert "https://api.bintray.com/conan/foo/bar" == builder.remotes_manager._upload.url
    assert 'False' == builder.remotes_manager._upload.use_ssl


def test_format_remote(set_remote_address):
    builder = build_autodetect._get_builder()
    remote = builder.remotes_manager._remotes[0]
    assert 1 == len(builder.remotes_manager._remotes)
    assert "remotefoo" == remote.name
    assert "https://api.bintray.com/conan/foo/bar" == remote.url
    assert False == remote.use_ssl


def test_format_multi_remotes(set_multi_remote_address):
    builder = build_autodetect._get_builder()
    assert 2 == len(builder.remotes_manager._remotes)
    remote = builder.remotes_manager._remotes[0]
    assert "remotefoo" == remote.name
    assert "https://api.bintray.com/conan/foo/bar" == remote.url
    assert remote.use_ssl
    remote = builder.remotes_manager._remotes[1]
    assert "remote1" == remote.name
    assert "https://api.bintray.com/conan/qux/baz" == remote.url
    assert True == remote.use_ssl


def test_format_mixed_remotes(set_mixed_remote_address):
    builder = build_autodetect._get_builder()
    assert 2 == len(builder.remotes_manager._remotes)
    remote = builder.remotes_manager._remotes[0]
    assert "remotefoo" == remote.name
    assert "https://api.bintray.com/conan/foo/bar" == remote.url
    assert False == remote.use_ssl
    remote = builder.remotes_manager._remotes[1]
    assert "remote1" == remote.name
    assert "https://api.bintray.com/conan/qux/baz" == remote.url
    assert True == remote.use_ssl


def test_default_remote_address(set_upload_address):
    builder = build_autodetect._get_builder()
    assert 2 == len(builder.remotes_manager._remotes)
    remote = builder.remotes_manager._remotes[0]
    assert "remotefoo" == remote.name
    assert "https://api.bintray.com/conan/foo/bar" == remote.url
    remote = builder.remotes_manager._remotes[1]
    assert "upload_repo" == remote.name
    assert "https://api.bintray.com/conan/bincrafters/public-conan" == remote.url
