# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_default
from conans import tools


def add_boost_shared(build, recipe=None):
    if build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe(recipe=recipe)
        build.options.update({
            'boost_*:shared':
            build.options[shared_option_name]
        })
    return build


def get_builder(shared_option_name=None,
                pure_c=False,
                dll_with_static_runtime=False,
                build_policy=None,
                cwd=None,
                **kwargs):

    recipe = build_shared.get_recipe_path(cwd)

    # Bincrafters default is to upload only when stable, but boost is an exception
    # Empty string allows boost packages upload for testing branch
    with tools.environment_append({"CONAN_UPLOAD_ONLY_WHEN_STABLE": ""}):
        shared_option_name = False if shared_option_name is None and not build_shared.is_shared() else shared_option_name

        builder = build_template_default.get_builder(
            shared_option_name=shared_option_name,
            pure_c=pure_c,
            dll_with_static_runtime=dll_with_static_runtime,
            build_policy=build_policy,
            cwd=cwd,
            **kwargs)
        builder.builds = map(lambda item : add_boost_shared(item, recipe=recipe), builder.items)

        return builder
