import click

from click_spinner import spinner
from github.Requester import Requester

from esu_cli.github import _params, github_tools

from esu_cli.utils.click_wrappers import MessageWithCheckMark


@click.command(name="tpv-link")
@_params.github_params
@click.option("-o", "--org", type=click.STRING, default=None, show_default=True)
@click.option("-r", "--repo", type=click.STRING, default=None, show_default=True)
@click.option("-n", "--num", type=click.INT, default=None, show_default=True)
@click.option("-f", "--filter", type=click.STRING)
def main(remote, org, repo, num, filter):
    """Response schema for all third party verification (statuses)"""
    base_url, token = github_tools.get_scm(remote)

    with MessageWithCheckMark(
        f"Connecting to GitHub; Base URL: {base_url or 'using public GitHub'}"
    ), spinner():
        g = github_tools.UserGithub(login_or_token=token, base_url=base_url)
        g_repo = g.get_repo(f"{org}/{repo}")

    pr = g_repo.get_pull(num)
    _ = pr.raw_data["_links"]["statuses"]["href"]
    status_link = _.get("statuses", None)

    if not links:
        click.Abort("No third party status found")
    click.secho("Links found", color="green")
    for link in links:
        click.secho(link)


if __name__ == "__main__":
    main(["--remote", "ford", "-o", "PHX-AOSP", "-r", "vendor-ford-packages-apps-Car-CarPlay", "-n", 236])

