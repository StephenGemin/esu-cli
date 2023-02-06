import click
import click_log

from esu_cli import __version__


@click.group()
@click_log.simple_verbosity_option()
@click.version_option(__version__)
def main():
    click.echo(f"ESU Command Line Interface version {__version__}")
    click.echo(err=True)


if __name__ == '__main__':
    main()
