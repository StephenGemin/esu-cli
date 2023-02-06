import functools

import click

try:
    from importlib.metadata import version, PackageNotFoundError
except (ImportError, ModuleNotFoundError):
    from importlib_metadata import version, PackageNotFoundError


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"


def git_params(func):
    @click.option(
        "-b",
        "--base",
        help="base branch from which the cherry-picked commit is coming from",
        type=click.STRING,
        required=True,
    )
    @click.option(
        "-f",
        "--force/--no-force",
        help="Force or update push to origin. Default is " "to update push.",
        is_flag=True,
        default=False,
        show_default=True,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
