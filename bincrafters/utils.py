import subprocess


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
    return _utils_execute_script("git branch --show-current")


def utils_git_get_current_commit() -> str:
    return _utils_execute_script("git rev-parse HEAD")


def utils_git_get_changed_dirs(base: str, head: str = None) -> list:
    if not head:
        # Per default lets get the diff between the provided base and the commit before that
        head = "{}^1".format(base)

    merge_base = _utils_execute_script("git merge-base {} {}".format(base, head))
    dirs = _utils_execute_script("git diff --dirstat=files,0 {}..{} | sed 's/^[ 0-9.]\\+% //g'".format(merge_base, head),
                                 remove_newlines=False)
    return dirs.splitlines()
