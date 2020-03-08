import os
import sys
import subprocess

from bincrafters.build_shared import get_recipe_path, printer, inspect_value_from_recipe, get_os
import bincrafters.build_template_default as build_template_default
import bincrafters.build_template_header_only as build_template_header_only
import bincrafters.build_template_installer as build_template_installer


_recipe_path = os.path.dirname(get_recipe_path())


def _file_contains(file, word):
    """ Read file and search for word

    :param file: File path to be read
    :param word: word to be found
    :return: True if found. Otherwise, False
    """
    if os.path.isfile(file):
        with open(file) as ifd:
            content = ifd.read()
            if word in content:
                return True
    return False


def _recipe_contains(word):
    return _file_contains(get_recipe_path(), word)


def _has_option(option_name):
    options = inspect_value_from_recipe(attribute="options", recipe_path=get_recipe_path())
    if options and option_name in options:
        return True

    return False


def _has_setting(setting_name):
    settings = inspect_value_from_recipe(attribute="settings", recipe_path=get_recipe_path())
    if settings and setting_name in settings:
        return True

    return False


def _flush_output():
    sys.stderr.flush()
    sys.stdout.flush()


def _is_custom_build_py_existing() -> (bool, str):
    custom_build_path = os.path.join(_recipe_path, "build.py")
    if os.path.isfile(custom_build_path):
        return True, custom_build_path

    return False, None


def _is_pure_c():
    if _recipe_contains("del self.settings.compiler.libcxx") and _recipe_contains("del self.settings.compiler.cppstd"):
        return True

    return False


def _is_conditional_header_only():
    return _has_option("header_only")


def _is_unconditional_header_only():
    if not _is_conditional_header_only() and _recipe_contains("self.info.header_only()"):
        return True

    return False


def _is_installer():
    if not _is_unconditional_header_only() and not _is_conditional_header_only():
        if (_recipe_contains("self.env_info.PATH.append") or _recipe_contains("self.env_info.PATH.extend")) \
            and _has_setting("os_build") and _has_setting("arch_build") and \
                (not _has_setting("compiler") or _recipe_contains("del self.info.settings.compiler")):
            return True

    return False


def run_autodetect():
    has_custom_build_py, custom_build_py_path = _is_custom_build_py_existing()

    if has_custom_build_py:
        printer.print_message("Custom build.py detected. Executing ...")
        _flush_output()
        subprocess.run(["python",  "{}".format(custom_build_py_path)], check=True)
        return

    is_installer = _is_installer()
    printer.print_message("Is the package an installer for executable(s)? {}"
                          .format(str(is_installer)))

    if not is_installer:
        is_unconditional_header_only = _is_unconditional_header_only()
        printer.print_message("Is the package header only? {}"
                              .format(str(is_unconditional_header_only)))

        if not is_unconditional_header_only:
            is_conditional_header_only = _is_conditional_header_only()
            printer.print_message("Is the package conditionally header only ('header_only' option)? {}"
                                  .format(str(is_conditional_header_only)))

            is_pure_c = _is_pure_c()
            printer.print_message("Is the package C-only? {}".format(str(is_pure_c)))

    _flush_output()

    if is_installer:
        arch = os.getenv("ARCH", "x86_64")
        builder = build_template_installer.get_builder()
        builder.add({"os": get_os(), "arch_build": arch, "arch": arch}, {}, {}, {})
        builder.run()
    elif is_unconditional_header_only:
        builder = build_template_header_only.get_builder()
        builder.run()
    else:
        builder = build_template_default.get_builder(pure_c=is_pure_c)
        builder.run()

