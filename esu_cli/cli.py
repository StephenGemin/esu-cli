import logging

import click
import click_log

from esu_cli import __version__
from esu_cli.github import github_subcommands

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
@click.version_option(__version__)
def main():
    click.echo(f"ESU Command Line Interface version {__version__}")
    click.echo(err=True)


main.add_command(github_subcommands)


if __name__ == "__main__":
    main()
