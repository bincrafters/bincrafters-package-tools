import argparse
import sys
import json

from bincrafters.build_autodetect import run_autodetect
from bincrafters.autodetect import autodetect
from bincrafters.generate_ci_jobs import generate_ci_jobs
from bincrafters.prepare_env import prepare_env


def _parse_arguments(*args):
    parser = argparse.ArgumentParser(description="Bincrafters Package Tools")
    parser.add_argument('--auto', action='store_true',
                        help="Executes builds according to current env variables and recipe type auto detection")
    subparsers = parser.add_subparsers(dest="commands")
    genmatrix = subparsers.add_parser("generate-ci-jobs", help="Provides a CI job matrix as a JSON-fied string")
    genmatrix.add_argument('--platform', type=str, choices=["gha", "azp"],
                        help="Specfies the CI platform")
    genmatrix.add_argument('--split-by-build-types', type=str, choices=["true", "false"],
                        help="Split build jobs by build types")
    prepareenv = subparsers.add_parser("prepare-env", help="Prepares the environment by setting env vars and similar")
    prepareenv.add_argument('--platform', type=str, required=True, choices=["gha", "azp"],
                        help="Specfies the CI platform")
    prepareenv.add_argument('--config', type=str, required=True,
                        help="JSON config string in the bincrafters-package-tools format")
    prepareenv.add_argument('--select-config', type=str, required=False,
                        help="AZP only; name which config pair gets applied")
    args = parser.parse_args(*args)
    return args


def run(*args):
    arguments = _parse_arguments(*args)
    if arguments.auto:
        run_autodetect()
    elif arguments.commands == "prepare-env":
        config = json.loads(arguments.config)
        prepare_env(platform=arguments.platform, config=config, select_config=arguments.select_config)
    elif arguments.commands == "generate-ci-jobs":
        split_by_build_types = arguments.split_by_build_types

        # Note: it is important that we only print the matrix and absolutely nothing else
        print(generate_ci_jobs(platform=arguments.platform, split_by_build_types=split_by_build_types))


def cli():
    run(sys.argv[1:])


if __name__ == '__main__':
    try:
        sys.exit(cli())
    except Exception as error:
        print("ERROR: {}".format(error))
        sys.exit(1)

