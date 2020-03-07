import os
import tempfile
import contextlib
import yaml

from bincrafters.build_shared import get_version, get_recipe_path, printer, inspect_value_from_recipe
import bincrafters.build_template_default as build_template_default
import bincrafters.build_template_header_only as build_template_header_only
from conans.util.files import load
from conans import tools


_tmp_dir = tempfile.mkdtemp(prefix="bincrafters-package-tools")
_recipe_path = os.path.dirname(get_recipe_path())


@contextlib.contextmanager
def chdir(newdir):
    """ Change directory using locked scope

    :param newdir: Temporary folder to move
    """
    old_path = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(old_path)


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


def _get_files_with_extensions(folder, extensions):
    files = []
    with tools.chdir(folder):
        for (root, _, filenames) in os.walk("."):
            for filename in filenames:
                for ext in [ext for ext in extensions if ext != ""]:
                    if filename.endswith(".%s" % ext):
                        files.append(os.path.join(root, filename))
                    # Look for possible executables
                    elif ("" in extensions and "." not in filename
                          and not filename.endswith(".") and "license" not in filename.lower()):
                        files.append(os.path.join(root, filename))
    return files


def _perform_downloads() -> list:
    conandata_file = load(os.path.join(_recipe_path, "conandata.yml"))
    conan_data = yaml.safe_load(conandata_file)

    version = get_version()

    downloads = conan_data["sources"][version]
    if isinstance(conan_data["sources"][version], dict):
        downloads = [conan_data["sources"][version], ]

    i = 0
    download_directories = []
    for download in downloads:
        print("Downloading {}".format(download["url"]))
        tmp_dir = os.path.join(_tmp_dir, str(i))
        os.mkdir(tmp_dir)
        with chdir(tmp_dir):
            tools.get(**download, retry=2, retry_wait=5)
        i += 1
        download_directories.append(tmp_dir)

    return download_directories


def _is_pure_c(download_directories):
    cpp_extensions = ["cc", "cpp", "cxx", "c++m", "cppm", "cxxm", "h++", "hh", "hxx", "hpp"]
    c_extensions = ["c", "h"]

    for download_dir in download_directories:
        if _get_files_with_extensions(download_dir, cpp_extensions) or \
                not _get_files_with_extensions(download_dir, c_extensions):
            return False

    return True


def _is_conditional_header_only():
    options = inspect_value_from_recipe(attribute="options", recipe_path=get_recipe_path())
    if options and "header_only" in options:
        return True

    return False


def _is_unconditional_header_only():
    if not _is_conditional_header_only() and _file_contains(get_recipe_path(), "self.info.header_only()"):
        return True

    return False


def run_autodetect():
    download_directories = _perform_downloads()

    is_unconditional_header_only = _is_unconditional_header_only()
    printer.print_message("Is the package header only? {}"
                          .format(str(is_unconditional_header_only)))

    if not is_unconditional_header_only:
        is_conditional_header_only = _is_conditional_header_only()
        printer.print_message("Is the package conditionally header only ('header_only' option)? {}"
                              .format(str(is_conditional_header_only)))

        is_pure_c = _is_pure_c(download_directories)
        printer.print_message("Is the package C-only? {}".format(str(is_pure_c)))

    if is_unconditional_header_only:
        builder = build_template_header_only.get_builder()
        builder.run()
    else:
        builder = build_template_default.get_builder(pure_c=is_pure_c)
        builder.run()
