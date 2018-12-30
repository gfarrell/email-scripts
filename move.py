import imaplib
import click
import time

BATCH_SIZE=250
REST_TIME=100/1000 # 100µs

def connect(server, user, password, folder):
    """Connects to the imap server"""
    client = imaplib.IMAP4_SSL(host=server, port=993)
    client.login(user, password)
    result = client.select("\"{}\"".format(folder))
    if result[0] != "OK":
        raise Exception("Unable to select folder {}".format(folder))
    return client

def disconnect(client):
    """Closes an IMAP connection"""
    client.close()
    client.logout()
    return True;

def get_uids(client):
    result, items = client.uid("search", None, "ALL")
    if items == [""]:
        return []
    else:
        return items[0].split()

def get_message_info(client, uid):
    """fetches some basic message info (useful for debugging)"""
    fields = "(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])"
    result, data = client.uid("fetch", uid, fields)
    if result != "OK":
        raise Exception("Unable to fetch info for message {}".format(uid))
    return data[0]

def exec_move(client, uids, to):
    """executes the move command for given messages in batches"""
    i = 0 # batch index number
    t = 0 # total done count
    for uid in uids:
        result = client._simple_command("UID", "MOVE", uid, to)
        if result[0] != "OK":
            raise Exception("Error moving message {} ... aborting".format(uid))
        i = (i + 1) % BATCH_SIZE
        t += 1
        if i == 0:
            print("DONE {}".format(t))
            time.sleep(REST_TIME)

@click.command()
@click.option("--server", "-s", help="IMAP server", required=True)
@click.option("--user", "-u", help="username", required=True)
@click.option("--password", "-p", help="password", required=True)
@click.option("--from", "-f", "ffrom", help="folder from which to move emails", required=True)
@click.option("--to", "-t", help="folder to which to move emails", required=True)
def move_emails(server, user, password, ffrom, to):
    """moves emails from one folder to another"""
    print("CONNECTING...")
    client = connect(server, user, password, ffrom)
    print("CONNECTED")
    print("FETCHING MESSAGES...")
    messages = get_uids(client)
    print("GOT {} MESSAGES IN {}".format(len(messages), ffrom))
    print("MOVING MESSAGES {} ~> {}".format(ffrom, to))
    exec_move(client, messages, to)
    print("DISCONNECTING...")
    disconnect(client)
    print("BYE")

if __name__ == "__main__":
    move_emails()
