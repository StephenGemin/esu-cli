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
