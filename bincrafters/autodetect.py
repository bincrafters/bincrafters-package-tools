import os
from bincrafters.build_shared import get_recipe_path, inspect_value_from_recipe

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


def recipe_contains(word):
    return _file_contains(get_recipe_path(), word)


def recipe_has_option(option_name):
    options = inspect_value_from_recipe(attribute="options", recipe_path=get_recipe_path())
    if options and option_name in options:
        return True

    return False


def recipe_has_setting(setting_name):
    settings = inspect_value_from_recipe(attribute="settings", recipe_path=get_recipe_path())
    if settings and setting_name in settings:
        return True

    return False


def is_custom_build_py_existing() -> (bool, str):
    custom_build_path = os.path.join(_recipe_path, "build.py")
    if os.path.isfile(custom_build_path):
        return True, custom_build_path

    return False, None


def is_pure_c():
    if recipe_contains("del self.settings.compiler.libcxx") and recipe_contains("del self.settings.compiler.cppstd"):
        return True

    return False


def is_conditional_header_only():
    return recipe_has_option("header_only")


def is_unconditional_header_only():
    if not is_conditional_header_only() and recipe_contains("self.info.header_only()"):
        return True

    return False


def is_installer():
    if not is_unconditional_header_only() and not is_conditional_header_only():
        if (recipe_contains("self.env_info.PATH.append") or recipe_contains("self.env_info.PATH.extend")) \
                and (not recipe_has_setting("compiler") or recipe_contains("del self.info.settings.compiler")):
            return True

    return False


def autodetect() -> str:
    if is_installer():
        return "installer"
    else:
        if is_unconditional_header_only():
            return "unconditional_header_only"
        else:
            if is_conditional_header_only():
                return "conditional_header_only"
            else:
                if is_pure_c():
                    return "pure_c_lib"
                else:
                    return "cxx_lib"
