import logging

from github import Github, PullRequest, Repository

from esu_cli.utils import config

logger = logging.getLogger(__name__)

def get_scm(key: str):
    github_config = config.get_config()["github"]
    if key == "public":
        return None, github_config["token"]
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
        self, title, head, base, body=None, template=True, draft=False,
    ) -> PullRequest:
        logger.debug(f"\tCreate new pull request in {self.repo.full_name}")
        pr = self.repo.create_pull(
            title=title, body=body, head=head, base=base, draft=draft
        )
        logger.debug(f"\tPull Request URL: {pr.html_url}")
        return pr

