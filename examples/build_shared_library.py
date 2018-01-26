#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default


if __name__ == "__main__":
    # Set True when the target is NOT pure C project
    pure_c = False
    builder = build_template_default.get_builder(pure_c=pure_c)
    builder.run()
