import json
import os


def generate_ci_jobs(platform: str, recipe_type: str, split_by_build_types: bool) -> str:
    if platform != "gha":
        return ""

    matrix = {}

    if split_by_build_types is None:
        split_by_build_types = os.getenv("splitByBuildTypes", False)

    if recipe_type == "installer":
        matrix["config"] = [
            {"name": "Installer Linux", "compiler": "GCC", "version": "7", "os": "ubuntu-18.04", "dockerImage": "conanio/gcc7-centos6"},
            {"name": "Installer Windows", "compiler": "VISUAL", "version": "16", "os": "windows-2019"},
            {"name": "Installer macOS", "compiler": "APPLE_CLANG", "version": "11.0", "os": "macos-10.15"}
        ]
    elif recipe_type == "unconditional_header_only":
        matrix["config"] = [
            {"name": "Header-only Linux", "compiler": "CLANG", "version": "8", "os": "ubuntu-18.04"},
            {"name": "Header-only Windows", "compiler": "VISUAL", "version": "16", "os": "windows-latest"}
        ]
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

    matrix_string = json.dumps(matrix)
    return matrix_string
