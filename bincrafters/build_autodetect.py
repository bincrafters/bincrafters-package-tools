import os
import tempfile
import contextlib
import yaml

from bincrafters.build_shared import get_version, get_recipe_path, printer
from bincrafters.build_template_default import get_builder
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


def run_autodetect():
    download_directories = _perform_downloads()

    is_pure_c = _is_pure_c(download_directories)
    printer.print_message("Is library C-only? {}".format(str(is_pure_c)))

    builder = get_builder(pure_c=is_pure_c)
    builder.run()
