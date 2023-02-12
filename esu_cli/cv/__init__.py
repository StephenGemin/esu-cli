import logging

import click
import click_log

from esu_cli.cv import thresh
from esu_cli.cv import bgr_mask
from esu_cli.cv import canny_thresh
from esu_cli.cv import hsv_mask

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
click_log.basic_config(logger)


@click.group(name="cv", chain=True)
def cv_subcommands():
    """Computer vision (opencv) subcommands"""


cv_subcommands.add_command(thresh.main)
cv_subcommands.add_command(bgr_mask.main)
cv_subcommands.add_command(canny_thresh.main)
cv_subcommands.add_command(hsv_mask.main)
