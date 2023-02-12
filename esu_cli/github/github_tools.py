import logging
import re

import github
from github import Github, PullRequest, Repository

from esu_cli.utils import config

logger = logging.getLogger(__name__)


def get_scm(key: str) -> tuple:
    github_config = config.get_config()["github"]
    if key == "public":
        return None, github_config["public"]["token"]
    else:
        scm = github_config[key]
        return scm["base_url"], scm["token"]


class UserGithub(Github):
    def __init__(self, login_or_token=None, base_url=None, **kwargs):
        if base_url is not None:
            kwargs["base_url"] = base_url
        super().__init__(login_or_token=login_or_token, **kwargs)


class GithubRepo:
    def __init__(self, repo: Repository):
        self.repo = repo

    def create_pull(
        self,
        title,
        head,
        base,
        body=None,
        draft=False,
    ) -> PullRequest:
        if body is None:
            body = self._find_default_template()
        pr = self.repo.create_pull(
            title=title, body=body, head=head, base=base, draft=draft
        )
        return pr

    def _find_default_template(self) -> str:
        logger.info("Attempt to find remote pull request template")
        pattern = "pull_request_template"
        try:
            contents = self.repo.get_contents(".github")
        except github.UnknownObjectException:
            contents = []
            logger.exception(
                "Error fetching remote pull request template"
                "\n\nPossible reasons could be:"
                "\n\t.github folder does not exist in remote repo\n"
            )

        for file in contents:
            if re.findall(pattern, file.path.lower(), flags=re.IGNORECASE):
                logger.info(f"Remote pull request template found: {file.path}")
                file_content = self.repo.get_contents(file.path)
                return file_content.decoded_content.decode("utf-8")
        logger.info("Unable to find remote pull request template")
        return ""
