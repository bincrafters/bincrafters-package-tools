import sys
import subprocess

from bincrafters.build_shared import printer, get_os
import bincrafters.build_template_default as build_template_default
import bincrafters.build_template_header_only as build_template_header_only
import bincrafters.build_template_installer as build_template_installer
from bincrafters.autodetect import *


def _flush_output():
    sys.stderr.flush()
    sys.stdout.flush()


def run_autodetect():
    has_custom_build_py, custom_build_py_path = is_custom_build_py_existing()

    if has_custom_build_py:
        printer.print_message("Custom build.py detected. Executing ...")
        _flush_output()
        subprocess.run(["python",  "{}".format(custom_build_py_path)], check=True)
        return

    recipe_is_installer = is_installer()
    printer.print_message("Is the package an installer for executable(s)? {}"
                          .format(str(recipe_is_installer)))

    if not is_installer:
        recipe_is_unconditional_header_only = is_unconditional_header_only()
        printer.print_message("Is the package header only? {}"
                              .format(str(recipe_is_unconditional_header_only)))

        if not is_unconditional_header_only:
            recipe_is_conditional_header_only = is_conditional_header_only()
            printer.print_message("Is the package conditionally header only ('header_only' option)? {}"
                                  .format(str(recipe_is_conditional_header_only)))

            recipe_is_pure_c = is_pure_c()
            printer.print_message("Is the package C-only? {}".format(str(recipe_is_pure_c)))

    _flush_output()

    if recipe_is_installer:
        arch = os.getenv("ARCH", "x86_64")
        builder = build_template_installer.get_builder()
        builder.add({"os": get_os(), "arch_build": arch, "arch": arch}, {}, {}, {})
        builder.run()
    elif recipe_is_unconditional_header_only:
        builder = build_template_header_only.get_builder()
        builder.run()
    else:
        builder = build_template_default.get_builder(pure_c=recipe_is_pure_c)
        builder.run()

