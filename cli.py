import click
from mailbox import Mailbox
from move import cmd_move

@click.group()
@click.option("--host", "-h", help="IMAP server", required=True)
@click.option("--user", "-u", help="username", required=True)
@click.option("--password", "-p", help="password", required=True, prompt=True, hide_input=True)
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, host, user, password, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    mailbox = Mailbox(debug)
    mailbox.connect(host, user, password)
    ctx.obj["mailbox"] = mailbox

@cli.command()
@click.option(
        "--from", "-f", "ffrom",
        help="folder from which to move emails",
        required=True
        )
@click.option("--to", "-t",
        help="folder to which to move emails",
        required=True
        )
@click.pass_context
def move(ctx, ffrom, to):
    """moves emails from one folder to another"""
    mailbox = ctx.obj["mailbox"]
    cmd_move(mailbox, ffrom, to)
    mailbox.disconnect()

@cli.command()
@click.option(
        "--source", "-s",
        help="folder in which to look for original messages",
        default="INBOX",
        show_default=True,
        )
@click.option(
        "--target", "-t",
        help="folder in which to look for duplicates (defaults to source)",
        default=None,
        show_default=False
        )
@click.option(
        "--dest", "-d",
        help="folder into which to dump duplicate messages",
        default="Duplicates",
        show_default=True
        )
def dedup(ctx, source, target, dest):
    """finds and removes duplicate messages"""
    if target is None:
        target = source
    mailbox = ctx.obj["mailbox"]
    cmd_dedup(mailbox, source, target, dest)
    mailbox.disconnect()

if __name__ == "__main__":
    cli(obj={})
