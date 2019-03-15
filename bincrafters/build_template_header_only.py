# -*- coding: utf-8 -*-

from bincrafters import build_shared


def get_builder(**kwargs):
    builder = build_shared.get_builder(**kwargs)

    builder.add()

    return builder
