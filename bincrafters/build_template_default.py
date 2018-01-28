#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_shared


def get_builder(args=None, shared_option_name=None, pure_c=True, dll_with_static_runtime=False):

    builder = build_shared.get_builder(args)
    if shared_option_name is None and build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe()

    builder.add_common_builds(
        shared_option_name=shared_option_name, 
        pure_c=pure_c, 
        dll_with_static_runtime=dll_with_static_runtime
    )

    return builder

