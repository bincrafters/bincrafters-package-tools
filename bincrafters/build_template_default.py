# -*- coding: utf-8 -*-

import inspect
from cpt.packager import ConanMultiPackager
from bincrafters import build_shared


def get_builder(shared_option_name=None,
                pure_c=True,
                dll_with_static_runtime=False,
                build_policy=None,
                cwd=None,
                **kwargs):
    recipe = build_shared.get_recipe_path(cwd)

    builder = build_shared.get_builder(build_policy, cwd=cwd, **kwargs)
    if shared_option_name is None and build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe(recipe=recipe)

    # Do not pass kwargs from ConanMultiPackager constructor to add_common_builds
    attributes = inspect.getfullargspec(ConanMultiPackager.__init__)
    for attribute in attributes.args:
        try:
            kwargs.pop(attribute)
        except:
            pass

    builder.add_common_builds(
        shared_option_name=shared_option_name,
        pure_c=pure_c,
        dll_with_static_runtime=dll_with_static_runtime,
        **kwargs)

    return builder
