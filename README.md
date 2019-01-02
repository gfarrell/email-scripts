# Email Management Scripts

    $ python cli.py --help

    Usage: cli.py [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --host TEXT       IMAP server  [required]
      -u, --user TEXT       username  [required]
      -p, --password TEXT   password  [required]
      --debug / --no-debug
      --help                Show this message and exit.

    Commands:
      move   moves emails from one folder to another

## MOVE emails between folders

If you need to move emails from one folder to another in a mailbox, one
way is to use a mail client, download all the emails, then drag them to
the other folder. I suspect most mail clients will use something like
`COPY` ... `EXPUNGE`, but even if they don't, downloading all those
message headers is a little inefficient (especially as the client will
have to resynchronise.

Instead, you can use this move script, which uses the IMAP4 `MOVE`
command. I used this to move around 30k messages from one folder to
another when I migrated from Google Mail to Runbox so it works pretty
well, and inserts a 100µs rest every 250 messages anyway.

Unfortunately I haven't found a reliable way to operate over a range of
`UID`s, so this executes the `MOVE` on a per-message basis, which makes
it a little slow. It reports progress every 250 messages.

### Usage

For example, when moving emails from Gmail's "All Mail" folder, to my newly
created "Archives" folder:

    $ python cli.py -h imap.server.com -u me move -f "[Gmail].All Mail" -t "Archives"

Leaving out the `-p` password option causes the programme to prompt you for a
password (which is better than leaving it in plaintext).
