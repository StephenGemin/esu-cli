import logging

import click
import click_log

from esu_cli.github.pull_request import create, tpv_links

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
click_log.basic_config(logger)


@click.group(name="pr", chain=True)
def pr_subcommands():
    """GitHub Pull Request subcommands"""


pr_subcommands.add_command(create.main)
pr_subcommands.add_command(tpv_links.main)
