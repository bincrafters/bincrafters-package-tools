#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_shared


def get_builder(args=None, pure_c=True):
    builder = build_shared.get_builder(args)

    shared_option_name = None
    if build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe()

    builder.add_common_builds(shared_option_name=shared_option_name, pure_c=pure_c)

    return builder
