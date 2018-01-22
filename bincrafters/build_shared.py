#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
import os
import re
import platform


def get_value_from_recipe(search_string, recipe="conanfile.py"):
    with open(recipe, "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result


def get_name_from_recipe():
    return get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''').groups()[0]


def get_version_from_recipe():
    return get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''').groups()[0]


def is_shared():
    match = get_value_from_recipe(r'''options.*=([\s\S]*?)(?=}|$)''')
    if match is None:
        return False
    return "shared" in match.groups()[0]


def is_ci_running():
    return (os.getenv("APPVEYOR_REPO_NAME", None) or os.getenv("TRAVIS_REPO_SLUG", None)) is not None


def get_repo_name_from_ci():
    reponame_a = os.getenv("APPVEYOR_REPO_NAME","")
    reponame_t = os.getenv("TRAVIS_REPO_SLUG","")
    return reponame_a if reponame_a else reponame_t


def get_repo_branch_from_ci():
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH","")
    repobranch_t = os.getenv("TRAVIS_BRANCH","")
    return repobranch_a if repobranch_a else repobranch_t


def get_ci_vars():
    reponame = get_repo_name_from_ci()
    reponame_split = reponame.split("/")

    repobranch = get_repo_branch_from_ci()
    repobranch_split = repobranch.split("/")

    username, _ = reponame_split if len(reponame_split) > 1 else ["",""]
    channel, version = repobranch_split if len(repobranch_split) > 1 else ["",""]
    return username, channel, version


def get_username_from_ci():
    username, _, _ = get_ci_vars()
    return username


def get_channel_from_ci():
    _, channel, _ = get_ci_vars()
    return channel


def get_version_from_ci():
    _, _, version = get_ci_vars()
    return version


def get_version():
    ci_ver = get_version_from_ci()
    recipe_ver = get_version_from_recipe()
    return ci_ver if ci_ver else recipe_ver


def get_conan_vars():
    username = os.getenv("CONAN_USERNAME", get_username_from_ci() or "bincrafters")
    channel = os.getenv("CONAN_CHANNEL", get_channel_from_ci())
    version = os.getenv("CONAN_VERSION", get_version())
    return username, channel, version


def get_user_repository(username):
    return "https://api.bintray.com/conan/{0}/public-conan".format(username.lower())


def get_conan_upload(username):
    return os.getenv("CONAN_UPLOAD", get_user_repository(username))


def get_conan_remotes(username):
    # While redundant, this moves upload remote to position 0.
    remotes = [get_conan_upload(username)]

    # Add bincrafters repository for other users, e.g. if the package would
    # require other packages from the bincrafters repo.
    bincrafters_user = "bincrafters"
    if username != bincrafters_user:
        remotes.append(get_user_repository(bincrafters_user))
    return remotes


def get_upload_when_stable():
    env_value = os.getenv("CONAN_UPLOAD_ONLY_WHEN_STABLE")
    return  True if env_value == None else env_value


def get_os():
    return platform.system().replace("Darwin", "Macos")


def get_builder(args=None):
    name = get_name_from_recipe()
    username, channel, version = get_conan_vars()
    reference = "{0}/{1}".format(name, version)
    upload = get_conan_upload(username)
    remotes = os.getenv("CONAN_REMOTES", get_conan_remotes(username))
    upload_when_stable = get_upload_when_stable()
    stable_branch_pattern = os.getenv("CONAN_STABLE_BRANCH_PATTERN", "stable/*")
    builder = ConanMultiPackager(
        args=args,
        username=username,
        channel=channel,
        reference=reference,
        upload=upload,
        remotes=remotes,
        upload_only_when_stable=upload_when_stable,
        stable_branch_pattern=stable_branch_pattern)

    return builder
