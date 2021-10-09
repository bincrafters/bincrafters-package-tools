import os
import re
import platform
from conans.client import conan_api
from cpt.packager import ConanMultiPackager
from cpt.tools import split_colon_env
from cpt.remotes import RemotesManager
# from cpt.ci_manager import *
from cpt.printer import Printer
from bincrafters.build_paths import BINCRAFTERS_REPO_URL, BINCRAFTERS_LOGIN_USERNAME, BINCRAFTERS_USERNAME, BINCRAFTERS_REPO_NAME

printer = Printer()
# ci_manager = CIManager(printer=printer)


def get_recipe_path(cwd=None):
    cwd = os.getenv("BPT_CWD", cwd)
    conanfile = os.getenv("CONAN_CONANFILE", "conanfile.py")
    if cwd is None:
        return os.path.abspath(conanfile)
    else:
        return os.path.abspath(os.path.join(cwd, conanfile))


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
    cwd = os.getcwd()
    result = None

    try:
        dir_name = os.path.dirname(recipe_path)
        conanfile_name = os.path.basename(recipe_path)
        if dir_name == "":
            dir_name = "./"
        os.chdir(dir_name)
        conan_instance, _, _ = conan_api.Conan.factory()
        inspect_result = conan_instance.inspect(path=conanfile_name, attributes=[attribute])
        result = inspect_result.get(attribute)
    except:
        pass

    os.chdir(cwd)
    return result


def get_name_from_recipe(recipe=None):
    name = inspect_value_from_recipe(attribute="name", recipe_path=recipe)
    return name or get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''', recipe=recipe).groups()[0]


def get_version_from_recipe(recipe=None):
    version = inspect_value_from_recipe(attribute="version", recipe_path=recipe)
    return version or get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''', recipe=recipe).groups()[0]


def is_shared(recipe=None):
    options = inspect_value_from_recipe(attribute="options", recipe_path=recipe)
    if options:
        return "shared" in options

    match = get_value_from_recipe(r'''options.*=([\s\S]*?)(?=}|$)''', recipe=recipe)
    if match is None:
        return False
    return "shared" in match.groups()[0]


def get_repo_name_from_ci():
    reponame_a = os.getenv("APPVEYOR_REPO_NAME", "")
    reponame_azp = os.getenv("BUILD_REPOSITORY_NAME", "")
    reponame_g = os.getenv("GITHUB_REPOSITORY", "")
    return reponame_a or reponame_azp or reponame_g


def get_repo_branch_from_ci():
    # TODO: Try one day again to migrate this to CPTs CI Manager
    # Since CPTs CI Managers varies in logic this break to much of the existing behaviour
    # in a first attempt (Croydon)
    # ~~Remove GHA special handling after CPT 0.32.0 is released~~
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH", "")
    repobranch_azp = os.getenv("BUILD_SOURCEBRANCH", "")
    if repobranch_azp.startswith("refs/pull/"):
        repobranch_azp = os.getenv("SYSTEM_PULLREQUEST_TARGETBRANCH", "")
    def _clean_branch(branch):
        return branch[11:] if branch.startswith("refs/heads/") else branch
    repobranch_azp = _clean_branch(repobranch_azp)
    repobranch_g = _clean_branch(os.getenv("GITHUB_REF", ""))
    if os.getenv("GITHUB_EVENT_NAME", "") == "pull_request":
        repobranch_g = os.getenv("GITHUB_BASE_REF", "")

    return repobranch_a or repobranch_azp or repobranch_g


def get_ci_vars():
    reponame = get_repo_name_from_ci()
    reponame_split = reponame.split("/")

    repobranch = get_repo_branch_from_ci()
    repobranch_split = repobranch.split("/")

    username, _ = reponame_split if len(reponame_split) == 2 else ["", ""]
    channel, version = repobranch_split if len(repobranch_split) == 2 else ["", ""]
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
    env_ver = os.getenv("CONAN_VERSION", None)
    ci_ver = get_version_from_ci()
    if env_ver:
        return env_ver
    elif ci_ver:
        return ci_ver
    else:
        return get_version_from_recipe(recipe=recipe)


def get_conan_vars(recipe=None, kwargs={}):
    # these fallbacks have to handle empty environment variables too!
    # this is the case for e.g. external pull request (i.e. no secrets available)
    # This combined with versioned branches, lead to the error
    # that the channel is defined but not the username and CPT fails
    if "CONAN_USERNAME" in os.environ and os.getenv("CONAN_USERNAME") != "":
        username_fallback = os.getenv("CONAN_USERNAME")
    else:
        username_fallback = get_username_from_ci() or BINCRAFTERS_USERNAME

    if "CONAN_LOGIN_USERNAME" in os.environ and os.getenv("CONAN_LOGIN_USERNAME") != "":
        login_username_fallback = os.getenv("CONAN_LOGIN_USERNAME")
    else:
        login_username_fallback = BINCRAFTERS_LOGIN_USERNAME

    username = kwargs.get("username", username_fallback)
    kwargs["channel"] = kwargs.get("channel", os.getenv("CONAN_CHANNEL", get_channel_from_ci()))
    version = get_version(recipe=recipe)

    kwargs["login_username"] = kwargs.get("login_username", login_username_fallback)
    kwargs["username"] = username

    return username, version, kwargs


def get_user_repository(username, repository_name):
    return "https://{0}.jfrog.io/artifactory/api/conan/{1}".format(username.lower(), repository_name)


def get_conan_upload(username):
    if os.getenv("BPT_NO_UPLOAD", "").lower() in ["true", "yes", "on", "1"]:
        return False

    upload = os.getenv("CONAN_UPLOAD")
    if upload:
        return upload.split('@') if '@' in upload else upload

    repository_name = os.getenv("BINTRAY_REPOSITORY", BINCRAFTERS_REPO_NAME)
    return get_user_repository(username, repository_name)


def get_conan_upload_param(username, kwargs):
    if not get_conan_upload(username):
        try:
            del kwargs["upload"]
        except:
            pass
        return kwargs
    if "upload" not in kwargs and get_conan_upload(username):
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
            remotes = [get_conan_upload(username)] if get_conan_upload(username) else []
            # Add bincrafters repository for other users, e.g. if the package would
            # require other packages from the bincrafters repo.
            bincrafters_user = BINCRAFTERS_USERNAME
            if username != bincrafters_user:
                if get_conan_upload(bincrafters_user):
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
    cwd = os.path.dirname(recipe)

    name = get_name_from_recipe(recipe=recipe)
    username, version, kwargs = get_conan_vars(recipe=recipe, kwargs=kwargs)
    kwargs = get_reference(name, version, kwargs)
    kwargs = get_conan_upload_param(username, kwargs)
    kwargs = get_conan_remotes(username, kwargs)
    kwargs = get_upload_when_stable(kwargs)
    kwargs = get_stable_branch_pattern(kwargs)
    kwargs = get_archs(kwargs)
    build_policy = os.getenv("CONAN_BUILD_POLICY", build_policy)

    builder = ConanMultiPackager(
        build_policy=build_policy,
        cwd=cwd,
        **kwargs)

    return builder
