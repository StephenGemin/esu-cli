import logging
import re
from urllib.parse import urlparse

import click
import click_spinner
from git import Repo

from esu_cli.utils.click_wrappers import MessageWithCheckMark

logger = logging.getLogger(__name__)


class GitRepo:

    def __init__(self, path=None):
        self.repo = Repo(path)
        self._origin = self.repo.remotes[0]
        self._url = next(self._origin.urls)
        self._org = None
        self._name = None

        # for convenience
        self._wd = self.repo.working_tree_dir if path is None else path
        logger.debug(f"Git directory: {self._wd}")
        self._git = self.repo.git

    @property
    def origin(self) -> str:
        return self._origin.name

    @property
    def url(self) -> str:
        return self._url

    @property
    def org(self):
        if not self._org:
            path = urlparse(self._url).path
            self._org = path.split("/")[1]
        return self._org

    @property
    def repo_name(self):
        if not self._name:
            path = urlparse(self._url).path
            self._name = re.split(r"/|\.", path)[-2]
        return self._name

    def push(self, branch: str, *, force=False):
        method = "-f" if force else "-u"
        with MessageWithCheckMark(
            f"Push to origin: '{branch}'. " f"Push method: '{method}'"
        ), click_spinner.spinner():
            self._git.push(method, str(self.repo.remotes[0]), branch)

    def checkout(self, branch: str):
        with MessageWithCheckMark(
            f"Checkout branch '{branch}'"
        ), click_spinner.spinner():
            self._git.checkout(branch)

    def checkout_and_pull(self, branch: str):
        self.check_untracked_and_stash()
        with MessageWithCheckMark(
            f"Checkout and pull branch: '{branch}'"
        ), click_spinner.spinner():
            self._git.checkout(branch)
            self._git.pull()

    def pull(self):
        with MessageWithCheckMark(
            f"Pull origin into active branch: '" f"{self.repo.head.ref.name}'"
        ), click_spinner.spinner():
            self._git.pull()

    def fetch(self):
        with MessageWithCheckMark("Fetch from remote"), click_spinner.spinner():
            self.repo.remotes.origin.fetch()

    def delete_branch(self, branch: str, local: bool):
        if local:
            with MessageWithCheckMark(
                f"Delete local branch: '{branch}'"
            ), click_spinner.spinner():
                self._git.branch("-D", branch)
        else:
            with MessageWithCheckMark(
                f"Delete remote branch: '{branch}'"
            ), click_spinner.spinner():
                self._git.push("-d", "origin", branch)

    def check_untracked_and_stash(self):
        if not self._git.diff() and not self._git.diff("--cached"):
            return
        styles = {"fg": "bright_red", "bold": True}
        click.secho("Untracked files found, save to stash.", **styles)
        stdout = self._git.stash("save")
        click.secho(f"\t{stdout}", **styles)

    def create_branch(self, branch: str, base: str):
        if branch in self.repo.heads:
            click.secho(
                f"Deleted existing local branch: '{branch}'",
                fg="bright_red",
                bold=True,
            )
            self._git.branch("-D", branch)

        with MessageWithCheckMark(f"Create branch '{branch}'"), click_spinner.spinner():
            self._git.checkout("-b", branch, base)
