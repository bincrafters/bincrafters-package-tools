import json
import os
import subprocess


def prepare_env(platform: str, config: json):
    if platform != "gha":
        raise ValueError("Only GitHub Actions is supported at this point.")

    subprocess.run("conan user", shell=True)

    def _set_env_variable(var_name: str, value: str):
        print("{} = {}".format(var_name, value))
        os.environ[var_name] = value
        if platform == "gha":
            subprocess.run(
                'echo "{}={}" >> $GITHUB_ENV'.format(var_name, value),
                shell=True
            )

    compiler = config["compiler"]
    compiler_version = config["version"]
    docker_image = config.get("docker_image", "")
    build_type = config.get("build_type", "")

    _set_env_variable("BPT_CWD", config["cwd"])
    _set_env_variable("CONAN_VERSION", config["recipe_version"])
    _set_env_variable("CONAN_{}_VERSIONS".format(compiler), compiler_version)

    if compiler == "GCC" or compiler == "CLANG":
        if docker_image == "":
            compiler_lower = compiler.lower()
            version_without_dot = compiler_version.replace(".", "")
            docker_image = "conanio/{}{}".format(compiler_lower, version_without_dot)
        _set_env_variable("CONAN_DOCKER_IMAGE", docker_image)

    if build_type != "":
        _set_env_variable("CONAN_BUILD_TYPES", build_type)

    if platform == "gha":
        if compiler == "APPLE_CLANG" and compiler_version == "11.0":
            subprocess.run(
                'sudo xcode-select -switch "/Applications/Xcode_11.3.1.app"',
                shell=True
            )
            subprocess.run(
                'clang++ --version',
                shell=True
            )

