import argparse
import sys

from bincrafters.build_autodetect import run_autodetect
from bincrafters.autodetect import autodetect
from bincrafters.generate_ci_jobs import generate_ci_jobs


def _parse_arguments(*args):
    parser = argparse.ArgumentParser(description="Bincrafters Package Tools")
    parser.add_argument('--auto', action='store_true',
                        help="Executes builds according to current env variables and recipe type auto detection")
    subparsers = parser.add_subparsers(dest="commands")
    genmatrix = subparsers.add_parser("generate-ci-jobs", help="Provides a CI job matrix as a JSON-fied string")
    genmatrix.add_argument('--platform', type=str, choices=["gha"],
                        help="Specfies the CI platform")
    genmatrix.add_argument('--split-by-build-types', type=str, choices=["true", "false"],
                        help="Split build jobs by build types")

    args = parser.parse_args(*args)
    return args


def run(*args):
    arguments = _parse_arguments(*args)
    if arguments.auto:
        run_autodetect()
    elif arguments.commands == "generate-ci-jobs":
        recipe_type = autodetect()
        split_by_build_types = arguments.split_by_build_types
        print(generate_ci_jobs(platform=arguments.platform, recipe_type=recipe_type, split_by_build_types=split_by_build_types))


def cli():
    run(sys.argv[1:])


if __name__ == '__main__':
    try:
        sys.exit(cli())
    except Exception as error:
        print("ERROR: {}".format(error))
        sys.exit(1)

