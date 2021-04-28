import os

MINIMUM_CONFIG_FILE_VERSIONS = {
    "generate-ci-jobs": {
        "gha": 11,
        "azp": 2
    }
}


def get_config_file_version() -> int:
    return int(os.getenv("BPT_CONFIG_FILE_VERSION", 0))


def get_minimum_compatible_version(platform: str, feature: str) -> int:
    if platform not in ["gha", "azp"]:
        raise ValueError("Unknown platform value {}".format(platform))

    if feature not in ["generate-ci-jobs", ]:
        raise ValueError("Unknown feature value {}".format(feature))

    return MINIMUM_CONFIG_FILE_VERSIONS[feature][platform]


def is_ci_config_compatible(platform: str, feature: str) -> bool:
    config_version = get_config_file_version()
    minimum_version = get_minimum_compatible_version(platform=platform, feature=feature)

    if config_version < minimum_version:
        return False

    return True
