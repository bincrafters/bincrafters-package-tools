#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default


def get_builder(args=None, shared_option_name=None, pure_c=False, dll_with_static_runtime=False):

    # Bincrafters default is to upload only when stable, but boost is an exception
    # Empty string allows boost packages upload for testing branch
    os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = ""

    return build_template_default.get_builder(args=args, shared_option_name="boost_*:shared", pure_c=pure_c, dll_with_static_runtime=dll_with_static_runtime)
