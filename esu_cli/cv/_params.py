import functools

import click


def image_process_params(func):
    @click.option(
        "--view-scale",
        help="Change the scale of the viewing window, helpful when trying to fit "
        "everything on your display",
        type=click.FLOAT,
        default=1.0,
        show_default=True,
    )
    @click.option(
        "--save-result",
        is_flag=True,
        flag_value=True,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
