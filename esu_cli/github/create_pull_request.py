import click
from click_spinner import spinner

from esu_cli import git_params
from esu_cli.git.git_repo import GitRepo
from esu_cli.github import github_tools

from esu_cli.utils.click_wrappers import MessageWithCheckMark


@click.command(name="create-pr")
@git_params
@click.option("--scm-key", type=click.STRING, default="public")
@click.option("-h", "--head", type=click.STRING, default=None)
@click.option("-o", "--org", type=click.STRING, default=None)
@click.option("-r", "--repo", type=click.STRING, default=None)
@click.option("-t", "--title", type=click.STRING, required=True)
def main(scm_key, base, force, head, org, repo, title):
    """Create new pull request in GitHub"""
    gr = GitRepo()

    base_url, token = github_tools.get_scm(scm_key)
    org = org or gr.org
    repo = repo or gr.repo

    with MessageWithCheckMark(f"Connecting to GitHub; {base_url}"), spinner():
        g = github_tools.UserGithub(login_or_token=token, base_url=base_url)
        g_repo = github_tools.GithubRepo(g.get_repo(f"{org}/{repo}"))

    with MessageWithCheckMark(f"Creating pull request"), spinner():
        g_repo.create_pull(title, head, base)

def other_main():
    return GitRepo()


if __name__ == '__main__':
    gr = other_main()
    t=1
