import os
import re
import platform
from conans.client import conan_api
from cpt.packager import ConanMultiPackager
from cpt.tools import split_colon_env
from cpt.remotes import RemotesManager
from bincrafters.build_paths import BINCRAFTERS_REPO_URL, BINCRAFTERS_LOGIN_USERNAME, BINCRAFTERS_USERNAME, BINCRAFTERS_REPO_NAME


def get_recipe_path(cwd=None):
    conanfile = os.getenv("CONAN_CONANFILE", "conanfile.py")
    if cwd is None:
        return conanfile
    else:
        return os.path.join(cwd, conanfile)


def get_bool_from_env(var_name, default="1"):
    val = os.getenv(var_name, default)
    return str(val).lower() in ("1", "true", "yes", "y")


def get_value_from_recipe(search_string, recipe=None):
    if recipe is None:
        recipe = get_recipe_path()
    with open(recipe, "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result


def inspect_value_from_recipe(attribute, recipe_path):
    try:
        conan_instance, _, _ = conan_api.Conan.factory()
        inspect_result = conan_instance.inspect(path=recipe_path, attributes=[attribute])
        return inspect_result.get(attribute)
    except:
        pass
    return None


def get_name_from_recipe(recipe=None):
    name = inspect_value_from_recipe(attribute="name", recipe_path=get_recipe_path())
    return name or get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''', recipe=recipe).groups()[0]


def get_version_from_recipe(recipe=None):
    version = inspect_value_from_recipe(attribute="version", recipe_path=get_recipe_path())
    return version or get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''', recipe=recipe).groups()[0]


def is_shared(recipe=None):
    options = inspect_value_from_recipe(attribute="options", recipe_path=get_recipe_path())
    if options:
        return "shared" in options

    match = get_value_from_recipe(r'''options.*=([\s\S]*?)(?=}|$)''', recipe=recipe)
    if match is None:
        return False
    return "shared" in match.groups()[0]


def is_ci_running():
    result = os.getenv("APPVEYOR_REPO_NAME", False) or \
             os.getenv("TRAVIS_REPO_SLUG", False) or \
             os.getenv("CIRCLECI", False) or \
             os.getenv("SYSTEM_TEAMFOUNDATIONCOLLECTIONURI", False) or \
             os.getenv("GITHUB_WORKFLOW", False)
    return result != False


def get_repo_name_from_ci():
    reponame_a = os.getenv("APPVEYOR_REPO_NAME", "")
    reponame_t = os.getenv("TRAVIS_REPO_SLUG", "")
    reponame_c = "%s/%s" % (os.getenv("CIRCLE_PROJECT_USERNAME", ""),
                            os.getenv("CIRCLE_PROJECT_REPONAME", ""))
    reponame_azp = os.getenv("BUILD_REPOSITORY_NAME", "")
    reponame_g = os.getenv("GITHUB_REPOSITORY", "")
    return reponame_a or reponame_t or reponame_c or reponame_azp or reponame_g


def get_repo_branch_from_ci():
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH", "")
    repobranch_t = os.getenv("TRAVIS_BRANCH", "")
    repobranch_c = os.getenv("CIRCLE_BRANCH", "")
    repobranch_azp = os.getenv("BUILD_SOURCEBRANCH", "")
    if repobranch_azp.startswith("refs/pull/"):
        repobranch_azp = os.getenv("SYSTEM_PULLREQUEST_TARGETBRANCH", "")
    def _clean_branch(branch):        
        return branch[11:] if branch.startswith("refs/heads/") else branch
    repobranch_azp = _clean_branch(repobranch_azp)
    repobranch_g = _clean_branch(os.getenv("GITHUB_REF", ""))
    if os.getenv("GITHUB_EVENT_NAME", "") == "pull_request":
        repobranch_g = os.getenv("GITHUB_BASE_REF", "")
    
    return repobranch_a or repobranch_t or repobranch_c or repobranch_azp or repobranch_g


def get_ci_vars():
    reponame = get_repo_name_from_ci()
    reponame_split = reponame.split("/")

    repobranch = get_repo_branch_from_ci()
    repobranch_split = repobranch.split("/")

    username, _ = reponame_split if len(reponame_split) > 1 else ["", ""]
    channel, version = repobranch_split if len(repobranch_split) > 1 else ["", ""]
    return username, channel, version


def get_username_from_ci():
    username, _, _ = get_ci_vars()
    return username


def get_channel_from_ci():
    _, channel, _ = get_ci_vars()
    return channel


def get_version_from_ci():
    _, _, version = get_ci_vars()
    return version


def get_version(recipe=None):
    ci_ver = get_version_from_ci()
    return ci_ver if ci_ver else get_version_from_recipe(recipe=recipe)


def get_conan_vars(recipe=None, kwargs={}):
    username = kwargs.get("username", os.getenv(
        "CONAN_USERNAME", get_username_from_ci() or BINCRAFTERS_USERNAME))
    kwargs["channel"] = kwargs.get("channel", os.getenv("CONAN_CHANNEL", get_channel_from_ci()))
    version = os.getenv("CONAN_VERSION", get_version(recipe=recipe))
    kwargs["login_username"] = kwargs.get("login_username", os.getenv(
        "CONAN_LOGIN_USERNAME", BINCRAFTERS_LOGIN_USERNAME))
    kwargs["username"] = username

    return username, version, kwargs


def get_user_repository(username, repository_name):
    return "https://api.bintray.com/conan/{0}/{1}".format(username.lower(), repository_name)


def get_conan_upload(username):
    upload = os.getenv("CONAN_UPLOAD")
    if upload:
        return upload.split('@') if '@' in upload else upload

    repository_name = os.getenv("BINTRAY_REPOSITORY", BINCRAFTERS_REPO_NAME)
    return get_user_repository(username, repository_name)


def get_conan_upload_param(username, kwargs):
    if "upload" not in kwargs:
        kwargs["upload"] = get_conan_upload(username)
    return kwargs


def get_conan_remotes(username, kwargs):
    remotes = None
    if "remotes" not in kwargs:
        remotes = os.getenv("CONAN_REMOTES")
        if remotes:
            remotes = remotes.split(',')
            for remote in reversed(remotes):
                if '@' in remote:
                    remote = RemotesManager._get_remote_from_str(remote, var_name=remote)
        else:
            # While redundant, this moves upload remote to position 0.
            remotes = [get_conan_upload(username)]
            # Add bincrafters repository for other users, e.g. if the package would
            # require other packages from the bincrafters repo.
            bincrafters_user = BINCRAFTERS_USERNAME
            if username != bincrafters_user:
                remotes.append(get_conan_upload(bincrafters_user))

            # Force Bincrafters repo on remotes
            if BINCRAFTERS_REPO_URL not in remotes:
                remotes.append(BINCRAFTERS_REPO_URL)

    kwargs["remotes"] = remotes
    return kwargs


def get_upload_when_stable(kwargs):
    upload_when_stable = kwargs.get('upload_only_when_stable')
    if upload_when_stable is None:
        kwargs['upload_only_when_stable'] = get_bool_from_env("CONAN_UPLOAD_ONLY_WHEN_STABLE")
    return kwargs


def get_os():
    return platform.system().replace("Darwin", "Macos")


def get_archs(kwargs):
    if "archs" not in kwargs:
        archs = os.getenv("CONAN_ARCHS", None)
        if archs is None:
            # Per default only build 64-bit artifacts
            kwargs["archs"] = ["x86_64"]
        else:
            kwargs["archs"] = split_colon_env("CONAN_ARCHS") if archs else None
    return kwargs


def get_stable_branch_pattern(kwargs):
    if "stable_branch_pattern" not in kwargs:
        kwargs["stable_branch_pattern"] = os.getenv("CONAN_STABLE_BRANCH_PATTERN", "stable/*")
    return kwargs


def get_reference(name, version, kwargs):
    if "reference" not in kwargs:
        kwargs["reference"] = "{0}/{1}".format(name, version)
    return kwargs


def get_builder(build_policy=None, cwd=None, **kwargs):
    recipe = get_recipe_path(cwd)
    name = get_name_from_recipe(recipe=recipe)
    username, version, kwargs = get_conan_vars(recipe=recipe, kwargs=kwargs)
    kwargs = get_reference(name, version, kwargs)
    kwargs = get_conan_upload_param(username, kwargs)
    kwargs = get_conan_remotes(username, kwargs)
    kwargs = get_upload_when_stable(kwargs)
    kwargs = get_stable_branch_pattern(kwargs)
    kwargs = get_archs(kwargs)
    build_policy = os.getenv('CONAN_BUILD_POLICY', build_policy)
    builder = ConanMultiPackager(
        build_policy=build_policy,
        cwd=cwd,
        **kwargs)

    return builder
