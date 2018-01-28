#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_default

def add_boost_shared(build):
    if build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe()
        build.options.update({'boost_*:shared' : build.options[shared_option_name]})
    return build

def get_builder(args=None, shared_option_name=None, pure_c=False, dll_with_static_runtime=False):

    # Bincrafters default is to upload only when stable, but boost is an exception
    # Empty string allows boost packages upload for testing branch
    os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = ""
    
    builder = build_template_default.get_builder(
        args=args, 
        shared_option_name=shared_option_name, 
        pure_c=pure_c, 
        dll_with_static_runtime=dll_with_static_runtime
    )
    
    builder.builds = map(add_boost_shared, builder.items)

    return builder