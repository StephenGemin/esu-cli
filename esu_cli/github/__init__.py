import logging

import click
import click_log

from esu_cli.github import create_pull_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
click_log.basic_config(logger)


@click.group(name="github", chain=True)
def github_subcommands():
    """GitHub subcommands"""


github_subcommands.add_command(create_pull_request.main)
