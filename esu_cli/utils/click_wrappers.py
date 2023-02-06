import click


class MessageWithCheckMark:
    def __init__(self, message, ok="+", fail="x"):
        self.message = message
        self.ok = ok
        self.fail = fail

    def __enter__(self):
        click.echo(self.message + " ", nl=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if all(v is None for v in [exc_type, exc_val, exc_tb]):
            click.secho(self.ok, fg="green")
        else:
            click.secho("{} ({})".format(self.fail, exc_val), fg="red")