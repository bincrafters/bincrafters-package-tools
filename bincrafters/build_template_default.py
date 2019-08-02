# -*- coding: utf-8 -*-

from bincrafters import build_shared


def get_builder(shared_option_name=None,
                pure_c=True,
                dll_with_static_runtime=False,
                build_policy=None,
                cwd=None,
                reference=None,
                **kwargs):
    recipe = build_shared.get_recipe_path(cwd)

    builder = build_shared.get_builder(build_policy, cwd=cwd, **kwargs)
    if shared_option_name is None and build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe(recipe=recipe)

    builder.add_common_builds(
        shared_option_name=shared_option_name,
        pure_c=pure_c,
        dll_with_static_runtime=dll_with_static_runtime,
        reference=reference)

    return builder
