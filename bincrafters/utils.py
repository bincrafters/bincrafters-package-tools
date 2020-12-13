import subprocess
import os


def _utils_execute_script(script: str, remove_newlines: bool = True) -> str:
    output = subprocess.run(script,
                            capture_output=True,
                            shell=True)
    result = output.stdout.decode("utf-8")
    if remove_newlines:
        result = output.stdout.decode("utf-8").replace("\n", "")
    return result


def utils_git_get_default_branch(remote: str = "origin") -> str:
    return _utils_execute_script("git remote show {} | grep 'HEAD branch' | sed 's/.*: //'".format(remote))


def utils_git_get_current_branch() -> str:
    def _clean_branch(branch):
        return branch[11:] if branch.startswith("refs/heads/") else branch

    repobranch_azp = os.getenv("BUILD_SOURCEBRANCHNAME", "")
    repobranch_gha = _clean_branch(os.getenv("GITHUB_REF", ""))
    if os.getenv("GITHUB_EVENT_NAME", "") == "pull_request":
        repobranch_gha = _clean_branch(os.getenv("GITHUB_HEAD_REF", ""))

    repobranch_git = _utils_execute_script("git branch --show-current")

    return repobranch_azp or repobranch_gha or repobranch_git


def utils_git_get_current_commit() -> str:
    return _utils_execute_script("git rev-parse HEAD")


def utils_git_get_changed_dirs(base: str, head: str = None) -> list:
    if not head:
        # Per default lets get the diff between the provided base and the commit before that
        head_merge_base = "{}^1".format(base)
        head = base
    else:
        head_merge_base = head

    merge_base = _utils_execute_script("git merge-base {} {}".format(base, head_merge_base))
    dirs = _utils_execute_script("git diff --dirstat=files,0 {}..{} | sed 's/^[ 0-9.]\\+% //g'".format(merge_base, head),
                                 remove_newlines=False)

    return dirs.splitlines()


def utils_file_contains(file, word):
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

