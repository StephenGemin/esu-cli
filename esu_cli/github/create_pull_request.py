import click
from click_spinner import spinner

from esu_cli.git.git_repo import GitRepo
from esu_cli.github import github_tools

from esu_cli.utils.click_wrappers import MessageWithCheckMark


@click.command(name="new-pr")
@click.option(
    "--remote",
    type=click.STRING,
    default="public",
    help="Only to be used if pushing to a non-public remote, Ex. enterprise",
    show_default=True,
)
@click.option("-b", "--base", type=click.STRING, required=True)
@click.option("-t", "--title", type=click.STRING, required=True)
@click.option("-h", "--head", type=click.STRING, default=None, show_default=True)
@click.option("-o", "--org", type=click.STRING, default=None, show_default=True)
@click.option("-r", "--repo", type=click.STRING, default=None, show_default=True)
@click.option(
    "-d", "--desc", help="Specify PR description/body", type=click.STRING, default=None
)
@click.option(
    "--push/--no-push",
    help="Push to remote before creating PR (no force)",
    is_flag=True,
    default=True,
    show_default=True,
)
@click.option("--draft", flag_value=True, default=False, show_default=True)
def main(remote, base, title, head, org, repo, desc, push, draft):
    """Create new pull request in GitHub"""
    gr = GitRepo()
    if not head:
        click.secho(
            "HEAD branch not passed, assume git details from cwd",
            fg="bright_red",
            bold=True,
        )
        head = head or gr.repo.head.ref.name

    org = org or gr.org
    repo = repo or gr.repo_name
    click.echo(f"\tHEAD: {head}")
    click.echo(f"\tORG: {org}")
    click.echo(f"\tREPO: {repo}")

    if push:
        gr.push(head)

    base_url, token = github_tools.get_scm(remote)

    with MessageWithCheckMark(
        f"Connecting to GitHub; Base URL: {base_url or 'using public GitHub'}"
    ), spinner():
        g = github_tools.UserGithub(login_or_token=token, base_url=base_url)
        g_repo = github_tools.GithubRepo(g.get_repo(f"{org}/{repo}"))

    with MessageWithCheckMark(f"Creating pull request", nl=True), spinner():
        pr = g_repo.create_pull(title, head, base, body=desc, draft=draft)
    click.secho(f"\tPull Request URL: {pr.html_url}")


if __name__ == "__main__":
    main(["-v", "DEBUG", "-b", "main", "-t", "foo"])
