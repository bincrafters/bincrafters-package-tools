# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_header_only
from conans import tools


def get_builder(**kwargs):

    with tools.environment_append({"CONAN_UPLOAD_ONLY_WHEN_STABLE": ""}):

        # Bincrafters default is to upload only when stable, but boost is an exception
        # Empty string allows boost packages upload for testing branch
        os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = ""

        return build_template_header_only.get_builder(**kwargs)
