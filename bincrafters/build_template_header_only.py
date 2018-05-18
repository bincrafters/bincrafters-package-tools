#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_shared


def get_builder(args=None, **kwargs):
    builder = build_shared.get_builder(args, **kwargs)

    builder.add()

    return builder
