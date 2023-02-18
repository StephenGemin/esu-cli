import functools

import click


def github_params(func):
    @click.option(
        "--remote",
        type=click.STRING,
        default="public",
        help="Only to be used if pushing to a non-public remote, Ex. enterprise",
        show_default=True,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
