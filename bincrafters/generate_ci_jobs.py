import json
import os
import yaml

from bincrafters.build_shared import get_bool_from_env, get_conan_vars, get_recipe_path, get_version_from_ci
from bincrafters.autodetect import *
from bincrafters.utils import *


def _run_macos_jobs_on_gha():
    if utils_file_contains("azure-pipelines.yml", "name: bincrafters/templates")\
            and utils_file_contains("azure-pipelines.yml", "template: .ci/azure.yml@templates"):
        return False

    if utils_file_contains(".travis.yml", "import: bincrafters/templates:.ci/travis"):
        return False

    return True


def _run_windows_jobs_on_gha():
    if utils_file_contains("azure-pipelines.yml", "name: bincrafters/templates")\
            and utils_file_contains("azure-pipelines.yml", "template: .ci/azure.yml@templates"):
        return False

    if utils_file_contains("appveyor.yml", "pip install bincrafters_package_tools"):
        return False

    return True


def generate_ci_jobs(platform: str, recipe_type: str = autodetect(), split_by_build_types: bool = False) -> str:
    if platform != "gha" and platform != "azp":
        return ""

    matrix = {}
    matrix_minimal = {}

    if split_by_build_types is None:
        # env var BPT_SPLIT_BY_BUILD_TYPES should be preferred over splitByBuildTypes (deprecated)
        split_by_build_types = get_bool_from_env("BPT_SPLIT_BY_BUILD_TYPES", get_bool_from_env("splitByBuildTypes", False))

    if platform == "gha":
        run_macos = _run_macos_jobs_on_gha()
        run_windows = _run_windows_jobs_on_gha()
        if recipe_type == "installer":
            matrix["config"] = [
                {"name": "Installer Linux", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "dockerImage": "conanio/gcc8"},
                {"name": "Installer Windows", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
                {"name": "Installer macOS", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macos-10.15"}
            ]
            matrix_minimal["config"] = matrix["config"].copy()
        elif recipe_type == "unconditional_header_only":
            matrix["config"] = [
                {"name": "Header-only Linux", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04"},
                {"name": "Header-only Windows", "compiler": "VISUAL", "version": "16", "os": "windows-latest"}
            ]
            matrix_minimal["config"] = matrix["config"].copy()
        else:
            if split_by_build_types:
                matrix["config"] = [
                    {"name": "GCC 4.9 Debug", "compiler": "GCC", "version": "4.9", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 4.9 Release", "compiler": "GCC", "version": "4.9", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "GCC 5 Debug", "compiler": "GCC", "version": "5", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 5 Release", "compiler": "GCC", "version": "5", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "GCC 6 Debug", "compiler": "GCC", "version": "6", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 6 Release", "compiler": "GCC", "version": "6", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "GCC 7 Debug", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 7 Release", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "GCC 8 Debug", "compiler": "GCC", "version": "8", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 8 Release", "compiler": "GCC", "version": "8", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "GCC 9 Debug", "compiler": "GCC", "version": "9", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 9 Release", "compiler": "GCC", "version": "9", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 3.9 Debug", "compiler": "CLANG", "version": "3.9", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 3.9 Release", "compiler": "CLANG", "version": "3.9", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 4.0 Debug", "compiler": "CLANG", "version": "4.0", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 4.0 Release", "compiler": "CLANG", "version": "4.0", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 5.0 Debug", "compiler": "CLANG", "version": "5.0", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 5.0 Release", "compiler": "CLANG", "version": "5.0", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 6.0 Debug", "compiler": "CLANG", "version": "6.0", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 6.0 Release", "compiler": "CLANG", "version": "6.0", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 7.0 Debug", "compiler": "CLANG", "version": "7.0", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 7.0 Release", "compiler": "CLANG", "version": "7.0", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 8 Debug", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 8 Release", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 9 Debug", "compiler": "CLANG", "version": "9", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 9 Release", "compiler": "CLANG", "version": "9", "os": "ubuntu-18.04", "buildType": "Release"}
                ]
                if run_macos:
                    matrix["config"] += [
                        {"name": "macOS Apple-Clang 10 Release", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.14", "buildType": "Release"},
                        {"name": "macOS Apple-Clang 10 Debug", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.14", "buildType": "Debug"},
                        {"name": "macOS Apple-Clang 11 Release", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Release"},
                        {"name": "macOS Apple-Clang 11 Debug", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Debug"},
                    ]
                if run_windows:
                    matrix["config"] += [
                        {"name": "Windows VS 2017 Release", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "buildType": "Release"},
                        {"name": "Windows VS 2017 Debug", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "buildType": "Debug"},
                        {"name": "Windows VS 2019 Release", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Release"},
                        {"name": "Windows VS 2019 Debug", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Debug"},
                    ]
                matrix_minimal["config"] = [
                    {"name": "GCC 7 Debug", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "GCC 7 Release", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "buildType": "Release"},
                    {"name": "CLANG 8 Debug", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04", "buildType": "Debug"},
                    {"name": "CLANG 8 Release", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04", "buildType": "Release"},
                ]
                if run_macos:
                    matrix_minimal["config"] += [
                        {"name": "macOS Apple-Clang 11 Debug", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Debug"},
                        {"name": "macOS Apple-Clang 11 Release", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Release"},
                    ]
                if run_windows:
                    matrix_minimal["config"] += [
                        {"name": "Windows VS 2019 Debug", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Debug"},
                        {"name": "Windows VS 2019 Release", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Release"},
                    ]
            else:
                matrix["config"] = [
                    {"name": "GCC 4.9", "compiler": "GCC", "version": "4.9", "os": "ubuntu-18.04"},
                    {"name": "GCC 5", "compiler": "GCC", "version": "5", "os": "ubuntu-18.04"},
                    {"name": "GCC 6", "compiler": "GCC", "version": "6", "os": "ubuntu-18.04"},
                    {"name": "GCC 7", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04"},
                    {"name": "GCC 8", "compiler": "GCC", "version": "8", "os": "ubuntu-18.04"},
                    {"name": "GCC 9", "compiler": "GCC", "version": "9", "os": "ubuntu-18.04"},
                    {"name": "CLANG 3.9", "compiler": "CLANG", "version": "3.9", "os": "ubuntu-18.04"},
                    {"name": "CLANG 4.0", "compiler": "CLANG", "version": "4.0", "os": "ubuntu-18.04"},
                    {"name": "CLANG 5.0", "compiler": "CLANG", "version": "5.0", "os": "ubuntu-18.04"},
                    {"name": "CLANG 6.0", "compiler": "CLANG", "version": "6.0", "os": "ubuntu-18.04"},
                    {"name": "CLANG 7.0", "compiler": "CLANG", "version": "7.0", "os": "ubuntu-18.04"},
                    {"name": "CLANG 8", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04"},
                    {"name": "CLANG 9", "compiler": "CLANG", "version": "9", "os": "ubuntu-18.04"},
                ]
                if run_macos:
                    matrix["config"] += [
                        {"name": "macOS Apple-Clang 10", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.14"},
                        {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
                    ]
                if run_windows:
                    matrix["config"] += [
                        {"name": "Windows VS 2017", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016"},
                        {"name": "Windows VS 2019", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
                    ]
                matrix_minimal["config"] = [
                    {"name": "GCC 7", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04"},
                    {"name": "CLANG 8", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04"},
                ]
                if run_macos:
                    matrix_minimal["config"] += [
                        {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
                    ]
                if run_windows:
                    matrix_minimal["config"] += [
                        {"name": "Windows VS 2019", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
                    ]
    elif platform == "azp":
        if split_by_build_types:
            matrix["config"] = [
                {"name": "macOS Apple-Clang 10 Release", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.14", "buildType": "Release"},
                {"name": "macOS Apple-Clang 10 Debug", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.14", "buildType": "Debug"},
                {"name": "macOS Apple-Clang 11 Release", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Release"},
                {"name": "macOS Apple-Clang 11 Debug", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Debug"},
                {"name": "Windows VS 2017 Release", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "buildType": "Release"},
                {"name": "Windows VS 2017 Debug", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016", "buildType": "Debug"},
                {"name": "Windows VS 2019 Release", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Release"},
                {"name": "Windows VS 2019 Debug", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Debug"},
            ]
            matrix_minimal["config"] = [
                {"name": "macOS Apple-Clang 11 Debug", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Debug"},
                {"name": "macOS Apple-Clang 11 Release", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15", "buildType": "Release"},
                {"name": "Windows VS 2019 Debug", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Debug"},
                {"name": "Windows VS 2019 Release", "compiler": "VISUAL", "version": "16", "os": "windows-2019", "buildType": "Release"},
            ]
        else:
            matrix["config"] = [
                {"name": "macOS Apple-Clang 10", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.14"},
                {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
                {"name": "Windows VS 2017", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016"},
                {"name": "Windows VS 2019", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
            ]
            matrix_minimal["config"] = [
                {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
                {"name": "Windows VS 2019", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
            ]

    directory_structure = autodetect_directory_structure()
    final_matrix = {"config": []}

    def _detect_changed_directories(path_filter: str = None) -> set:
        changed_dirs = []
        current_commit = utils_git_get_current_commit()
        current_branch = utils_git_get_current_branch()
        default_branch = utils_git_get_default_branch()

        changed_dirs.extend(utils_git_get_changed_dirs(base=current_commit))

        if default_branch != current_branch:
            # The default branch might not be tracked locally
            # i.e. "main" might be unknown, while "origin/main" should always be known
            # similar for the current_branch, so lets use the hash commit which should be always be known
            changed_dirs.extend(utils_git_get_changed_dirs(base="origin/{}".format(default_branch), head=current_commit))

        if path_filter:
            # Only list directories which start with a certain path
            # It also removes this filter prefix from the path
            # e.g. only get changed directories in recipes/ and remove recipes/ from results
            changed_dirs = [x.replace(path_filter, "") for x in changed_dirs if path_filter in x]

        # Remove trailing /
        changed_dirs = [os.path.dirname(x) for x in changed_dirs]

        return set(changed_dirs)

    def _parse_recipe_directory(path: str, path_filter: str = None, recipe_displayname: str = None):
        changed_dirs = _detect_changed_directories(path_filter=path_filter)
        config_file = os.path.join(path, "config.yml")
        config_yml = yaml.load(open(config_file, "r"))
        for version, version_attr in config_yml["versions"].items():
            version_build_value = version_attr.get("build", "full")
            # If we are on a branch like testing/3.0.0 then only build 3.0.0
            # regardless of config.yml settings
            # If we are on an unversioned branch, only build versions which dirs got changed
            if (get_version_from_ci() == "" and version_attr["folder"] in changed_dirs)\
                    or get_version_from_ci() == version:
                if version_build_value != "none":
                    if version_build_value == "full":
                        working_matrix = matrix.copy()
                    elif version_build_value == "minimal":
                        working_matrix = matrix_minimal.copy()
                    else:
                        raise ValueError("Unknown build value for version {} detected!".format(version))

                    for build_config in working_matrix["config"]:
                        new_config = build_config.copy()
                        if not path_filter:
                            new_config["cwd"] = version_attr["folder"]
                            new_config["name"] = "{} {}".format(version, new_config["name"])
                        else:
                            new_config["cwd"] = "{}{}".format(path_filter, version_attr["folder"])
                            new_config["name"] = "{}/{} {}".format(recipe_displayname, version, new_config["name"])
                        new_config["recipe_version"] = version
                        final_matrix["config"].append(new_config)

    if directory_structure == DIR_STRUCTURE_ONE_RECIPE_ONE_VERSION:
        for build_config in matrix["config"]:
            new_config = build_config.copy()
            new_config["cwd"] = "./"
            _, fixed_version, _ = get_conan_vars(recipe=get_recipe_path())
            new_config["recipe_version"] = fixed_version
            final_matrix["config"].append(new_config)

    elif directory_structure == DIR_STRUCTURE_ONE_RECIPE_MANY_VERSIONS:
        _parse_recipe_directory(path=os.getcwd())

    elif directory_structure == DIR_STRUCTURE_CCI:
        recipes = [f.path for f in os.scandir("recipes") if f.is_dir()]
        for recipe_folder in recipes:
            # the path_filter should end with a / so that the results don't start with one
            recipe_displayname = recipe_folder.replace("recipes/", "")
            _parse_recipe_directory(path=recipe_folder,
                                    path_filter="{}/".format(recipe_folder),
                                    recipe_displayname=recipe_displayname)

    # Now where we have to complete matrix, we have to parse them in a final string
    # which can be understood by the target platform
    matrix_string = "{}"

    if platform == "gha":
        matrix_string = json.dumps(final_matrix)
    elif platform == "azp":
        platform_matrix = {}
        for build_config in final_matrix["config"]:
            platform_matrix[build_config["name"]] = build_config
        matrix_string = json.dumps(platform_matrix)

    return matrix_string
