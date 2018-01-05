#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_shared


def get_builder(args=None):
    builder = build_shared.get_builder(args)

    builder.add()

    return builder
