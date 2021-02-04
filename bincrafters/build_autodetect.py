import sys
import subprocess
import tempfile
import os

from bincrafters.build_shared import printer, get_os
import bincrafters.build_template_default as build_template_default
import bincrafters.build_template_header_only as build_template_header_only
import bincrafters.build_template_installer as build_template_installer
from bincrafters.autodetect import *


def _flush_output():
    sys.stderr.flush()
    sys.stdout.flush()


def run_autodetect():
    ###
    # Enabling Conan download cache
    ###
    printer.print_message("Enabling Conan download cache ...")

    tmpdir = os.path.join(tempfile.gettempdir(), "conan")

    os.makedirs(tmpdir, mode=0o777)
    # In some cases Python may ignore the mode of makedirs, do it again explicitly with chmod
    os.chmod(tmpdir, mode=0o777)

    os.system('conan config set storage.download_cache="{}"'.format(tmpdir))
    os.system('conan config set general.revisions_enabled=1')
    os.environ["CONAN_DOCKER_ENTRY_SCRIPT"] =\
        "conan config set storage.download_cache='{}'; conan config set general.revisions_enabled=1".format(tmpdir)
    os.environ["CONAN_DOCKER_RUN_OPTIONS"] = "-v '{}':'/tmp/conan'".format(tmpdir)

    ###
    # Enabling installing system_requirements
    ###
    os.environ["CONAN_SYSREQUIRES_MODE"] = "enabled"

    ###
    # Detect and execute custom build.py file if existing
    ###
    has_custom_build_py, custom_build_py_path = is_custom_build_py_existing()

    if has_custom_build_py:
        printer.print_message("Custom build.py detected. Executing ...")
        _flush_output()

        new_wd = os.path.dirname(custom_build_py_path)
        if new_wd == "":
            new_wd = ".{}".format(os.sep)

        # build.py files have no knowledge about the directory structure above them.
        # Delete the env variable or BPT is appending the path a second time
        # when build.py calls BPT
        if "BPT_CWD" in os.environ:
            del os.environ["BPT_CWD"]

        subprocess.run("python build.py", cwd=new_wd, shell=True, check=True)
        return

    ###
    # Output collected recipe information in the builds logs
    ###
    recipe_is_installer = is_installer()
    printer.print_message("Is the package an installer for executable(s)? {}"
                          .format(str(recipe_is_installer)))

    if not recipe_is_installer:
        recipe_is_unconditional_header_only = is_unconditional_header_only()
        printer.print_message("Is the package header only? {}"
                              .format(str(recipe_is_unconditional_header_only)))

        if not recipe_is_unconditional_header_only:
            recipe_is_conditional_header_only = is_conditional_header_only()
            printer.print_message("Is the package conditionally header only ('header_only' option)? {}"
                                  .format(str(recipe_is_conditional_header_only)))

            recipe_is_pure_c = is_pure_c()
            printer.print_message("Is the package C-only? {}".format(str(recipe_is_pure_c)))

    _flush_output()

    ###
    # Start the build
    ###
    kwargs = {}

    if autodetect_directory_structure() == DIR_STRUCTURE_ONE_RECIPE_MANY_VERSIONS \
            or autodetect_directory_structure() == DIR_STRUCTURE_CCI:
        kwargs["stable_branch_pattern"] = os.getenv("CONAN_STABLE_BRANCH_PATTERN", "main")

    if recipe_is_installer:
        arch = os.getenv("ARCH", "x86_64")
        builder = build_template_installer.get_builder(**kwargs)
        builder.add({"os": get_os(), "arch_build": arch, "arch": arch}, {}, {}, {})
        builder.run()
    elif recipe_is_unconditional_header_only:
        builder = build_template_header_only.get_builder(**kwargs)
        builder.run()
    else:
        builder = build_template_default.get_builder(pure_c=recipe_is_pure_c, **kwargs)
        builder.run()

