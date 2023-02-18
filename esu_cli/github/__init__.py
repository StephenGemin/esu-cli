import logging

import click
import click_log

from esu_cli.github.pull_request import pr_subcommands

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
click_log.basic_config(logger)


@click.group(name="github")
def github_subcommands():
    """GitHub subcommands"""


github_subcommands.add_command(pr_subcommands)
