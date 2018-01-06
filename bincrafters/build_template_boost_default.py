#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default


def get_builder(args=None, pure_c=True):

    # Bincrafters default is to upload only when stable, but boost is an exception
    # Empty string allows boost packages upload for testing branch
    os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = ""

    return build_template_default.get_builder(args, pure_c)
