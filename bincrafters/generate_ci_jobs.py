import json
import os
from sys import version
import yaml
import copy

from bincrafters.build_shared import get_bool_from_env, get_conan_vars, get_recipe_path, get_version_from_ci, get_archs
from bincrafters.autodetect import *
from bincrafters.utils import *
from bincrafters.check_compatibility import *
import bincrafters

from cpt.tools import split_colon_env


def _run_macos_jobs_on_gha():
    if utils_file_contains("azure-pipelines.yml", "name: bincrafters/templates") \
            and utils_file_contains("azure-pipelines.yml", "template: .ci/azure.yml@templates"):
        return False

    return True


def _run_windows_jobs_on_gha():
    if utils_file_contains("azure-pipelines.yml", "name: bincrafters/templates") \
            and utils_file_contains("azure-pipelines.yml", "template: .ci/azure.yml@templates"):
        return False

    if utils_file_contains("appveyor.yml", "pip install bincrafters_package_tools"):
        return False

    return True

def _generate_gcc_matrices(archs, versions):
    gcc_matrix = {}
    gcc_matrix["config"] = []
    for v in versions:
        if v == "4.9":
            gcc_matrix["config"].extend(_generate_gcc4_9_matrix(archs))
        if v == "5":
            gcc_matrix["config"].extend(_generate_gcc5_matrix(archs))
        if v == "6":
            gcc_matrix["config"].extend(_generate_gcc6_matrix(archs))
        if v == "7":
            gcc_matrix["config"].extend(_generate_gcc7_matrix(archs))
        if v == "8":
            gcc_matrix["config"].extend(_generate_gcc8_matrix(archs))
        if v == "9":
            gcc_matrix["config"].extend(_generate_gcc9_matrix(archs))
        if v == "10":
            gcc_matrix["config"].extend(_generate_gcc10_matrix(archs))
    return gcc_matrix["config"]

def _generate_gcc_matrix(archs, version, valid_gcc_archs):
    gcc_matrix = []
    gcc_archs = [x for x in archs if x in valid_gcc_archs]
    for arch in gcc_archs:
        gcc_matrix.append(
            {"name": "GCC "+ version + " " + arch, "compiler": "GCC",
                "version": version, "os": "ubuntu-18.04", "arch": arch}
        )
    return gcc_matrix

def _generate_gcc4_9_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "x86", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"4.9",valid_gcc_archs)
    return matrix

def _generate_gcc5_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"5",valid_gcc_archs)
    return matrix

def _generate_gcc6_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"6",valid_gcc_archs)
    return matrix

def _generate_gcc7_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"7",valid_gcc_archs)
    return matrix

def _generate_gcc8_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"8",valid_gcc_archs)
    return matrix

def _generate_gcc9_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"9",valid_gcc_archs)
    return matrix

def _generate_gcc10_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "x86_64"])
    matrix = _generate_gcc_matrix(archs,"10",valid_gcc_archs)
    return matrix

def _generate_clang_matrix(archs, version, valid_archs):
    valid_clang_archs = set(valid_archs)
    
    clang_matrix = {}
    clang_matrix["config"] = []

    clang_archs = [x for x in archs if x in valid_clang_archs]

    for arch in clang_archs:
        clang_matrix["config"].append(
            {"name": "CLANG "+ version + " " + arch, "compiler": "CLANG",
            "version": version, "os": "ubuntu-18.04", "arch": arch}
        )
    return clang_matrix["config"]

def _generate_macos_clang_matrix(archs, version, valid_archs):
    valid_clang_archs = set(valid_archs)

    clang_matrix = {}
    clang_matrix["config"] = []

    clang_archs = [x for x in archs if x in valid_clang_archs]

    for arch in clang_archs:
        clang_matrix["config"].append(
            {"name": "macOS Apple-Clang "+ version+ " " + arch, "compiler": "APPLE_CLANG", 
            "version": version, "os": "macOS-10.15", "arch": arch}
        )
    return clang_matrix["config"]

def _generate_vs2017_matrix(archs, valid_archs):
    valid_vs2017_archs = set(valid_archs)
    
    vs2017_matrix = {}
    vs2017_matrix["config"] = []
    
    vs2017_archs = [x for x in archs if x in valid_vs2017_archs]

    for arch in vs2017_archs:
        vs2017_matrix["config"].append(
            {"name": "Windows VS 2017 "+ arch, "compiler": "VISUAL", 
            "version": "15", "os": "vs2017-win2016", "arch": arch},
        )
    return vs2017_matrix["config"]

def _generate_vs2019_matrix(archs, valid_archs):
    valid_vs2019_archs = set(valid_archs)
    
    vs2019_matrix = {}
    vs2019_matrix["config"] = []
    
    vs2019_archs = [x for x in archs if x in valid_vs2019_archs]

    for arch in vs2019_archs:
        vs2019_matrix["config"].append(
            {"name": "Windows VS 2019 " + arch, "compiler": "VISUAL", 
            "version": "16", "os": "windows-2019", "arch": arch},
        )
    return vs2019_matrix["config"]

def _get_base_config(recipe_directory: str, platform: str, split_by_build_types: bool, build_set: str = "full", recipe_type: str = ""):
    if recipe_type == "":
        cwd = os.getcwd()
        os.chdir(recipe_directory)
        recipe_type = autodetect()
        os.chdir(cwd)

    matrix = {}
    matrix_minimal = {}

    if platform == "gha":
        run_macos = _run_macos_jobs_on_gha()
        run_windows = _run_windows_jobs_on_gha()
        if recipe_type == "installer":
            matrix["config"] = [
                {"name": "Installer Linux", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "dockerImage": "conanio/gcc7"},
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
            matrix["config"] = []
            archs = split_colon_env("BPT_CONAN_ARCHS")
            matrix["config"].extend(
                _generate_gcc_matrix(archs, "4.9", ["x86","x86_64","armv7","armv7hf"]) +
                _generate_gcc_matrix(archs, "5", ["x86","x86_64","armv7","armv7hf","armv8"]) +
                _generate_gcc_matrix(archs, "6", ["x86","x86_64","armv7","armv7hf","armv8"]) +
                _generate_gcc_matrix(archs, "7", ["x86","x86_64","armv7","armv7hf","armv8"]) +
                _generate_gcc_matrix(archs, "8", ["x86","x86_64","armv7","armv7hf","armv8"]) +
                _generate_gcc_matrix(archs, "9", ["x86","x86_64","armv7","armv7hf","armv8"]) +
                _generate_gcc_matrix(archs, "10", ["x86_64","armv7","armv7hf"])
            )

            matrix["config"].extend(
                _generate_clang_matrix(archs, "3.9", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "4.0", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "5.0", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "6.0", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "7.0", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "8", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "9", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "10", ["x86","x86_64"]) +
                _generate_clang_matrix(archs, "11", ["x86","x86_64"])
            )

            if run_macos:
                matrix["config"].extend(
                    _generate_macos_clang_matrix(archs, "10.0", ["x86_64"]) +
                    _generate_macos_clang_matrix(archs, "11.0", ["x86_64"]) +
                    _generate_macos_clang_matrix(archs, "12.0", ["x86_64"])
                )

            if run_windows:
                matrix["config"].extend(
                    _generate_vs2017_matrix(archs, ["x86", "x86_64", "armv7"]) +
                    _generate_vs2019_matrix(archs, ["x86", "x86_64", "armv7", "armv8"])
                )

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
        matrix["config"] = [
            {"name": "macOS Apple-Clang 10", "compiler": "APPLE_CLANG", "version": "10.0", "os": "macOS-10.15"},
            {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
            {"name": "macOS Apple-Clang 12", "compiler": "APPLE_CLANG", "version": "12.0", "os": "macOS-10.15"},
            {"name": "Windows VS 2017", "compiler": "VISUAL", "version": "15", "os": "vs2017-win2016"},
            {"name": "Windows VS 2019", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
        ]
        matrix_minimal["config"] = [
            {"name": "macOS Apple-Clang 11", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macOS-10.15"},
            {"name": "Windows VS 2019", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
        ]

    # Split build jobs by build_type (Debug, Release)
    # Duplicate each builds job, then add the buildType value
    if split_by_build_types is None:
        # env var BPT_SPLIT_BY_BUILD_TYPES should be preferred over splitByBuildTypes (deprecated)
        split_by_build_types = get_bool_from_env("BPT_SPLIT_BY_BUILD_TYPES",
                                                 get_bool_from_env("splitByBuildTypes", False))

    if split_by_build_types:
        matrix_tmp = copy.deepcopy(matrix)
        matrix_minimal_tmp = copy.deepcopy(matrix_minimal)

        for m_tmp, m in [[matrix_tmp, matrix], [matrix_minimal_tmp, matrix_minimal]]:
            for i, config_set in enumerate(m_tmp["config"], start=0):
                m["config"].insert((i * 2) + 1, config_set.copy())
            for config_set in m["config"][0::2]:
                config_set["name"] = "{} Release".format(config_set["name"])
                config_set["buildType"] = "Release"
            for config_set in m["config"][1::2]:
                config_set["name"] = "{} Debug".format(config_set["name"])
                config_set["buildType"] = "Debug"

    if build_set == "full":
        return matrix
    elif build_set == "minimal":
        return matrix_minimal
    else:
        return {"config": []}


def generate_ci_jobs(platform: str, recipe_type: str = autodetect(), split_by_build_types: bool = False) -> str:
    if platform != "gha" and platform != "azp":
        return ""

    if not is_ci_config_compatible(platform=platform, feature="generate-ci-jobs"):
        raise Exception(
            "bincrafters-package-tools {} requires a newer {} CI config file; minimum version {} - current version {}".format(
                bincrafters.__version__,
                platform,
                get_minimum_compatible_version(platform=platform, feature="generate-ci-jobs"),
                get_config_file_version()
            ))

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
            if (get_version_from_ci() == "" and version_attr["folder"] in changed_dirs) \
                    or get_version_from_ci() == version:
                if version_build_value != "none":
                    if version_build_value == "full" or version_build_value == "minimal":
                        working_matrix = _get_base_config(
                            recipe_directory=os.path.join(path, version_attr["folder"]),
                            platform=platform,
                            split_by_build_types=split_by_build_types,
                            build_set=version_build_value
                        )
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
        matrix = _get_base_config(recipe_directory=".", platform=platform, split_by_build_types=split_by_build_types)
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

    # Now where we have the complete matrix, we have to parse it in a final string
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
