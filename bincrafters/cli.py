import argparse
import sys

from bincrafters.build_autodetect import run_autodetect


def _parse_arguments(*args):
    parser = argparse.ArgumentParser(description="Bincrafters Package Tools")
    parser.add_argument('--auto', action='store_true', default=True,
                        help="Enable autodetect if library is C or C++ only. Further detection is added in the future")

    args = parser.parse_args(*args)
    return args


def run(*args):
    arguments = _parse_arguments(*args)
    if arguments.auto:
        run_autodetect()


def cli():
    run(sys.argv[1:])


if __name__ == '__main__':
    run(sys.argv[1:])

