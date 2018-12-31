import imaplib
from mailbox.exceptions import *

class Mailbox:
    """Handles common IMAP operations"""

    def __init__(self, debug=False):
        self._DEBUG = debug

    def log(self, message, *substitutions):
        """Debug logging"""
        if self._DEBUG:
            print(message.format(*substitutions))

    def connect(self, host, user, password):
        """Connects to the IMAP host"""
        self.log("CONNECTING TO {}...", host)
        self.client = imaplib.IMAP4_SSL(host=host, port=993)
        self.client.login(user, password)
        self.log("CONNECTED")

    def disconnect(self):
        """Closes an IMAP connection"""
        self.log("DISCONNECTING...")
        self.client.close()
        self.client.logout()
        self.log("BYE BYE")

    def open_folder(self, folder):
        """Handles selecting a folder with error handling"""
        if folder is None:
            return
        self.log("OPENING FOLDER {}", folder)
        result = self.client.select(folder)
        if result[0] != "OK":
            raise IMAPFolderException(folder)

    def get_all_uids(self, folder=None):
        """Gets the UIDs of all the messages in a folder"""
        self.log("FETCHING MESSAGES IN {}...", folder)
        self.open_folder(folder)
        result, items = self.client.uid("SEARCH", None, "ALL")
        if result != "OK":
            raise IMAPCommandException("SEARCH", None, "ALL")
        if items == [""]:
            messages = []
        else:
            messages = items[0].split()
        self.log("GOT {} MESSAGES IN {}", len(messages), folder)
        return messages

    def move_message(self, uid, dest):
        """Moves a message to a different mailbox"""
        result = self.client._simple_command("UID", "MOVE", uid, dest)
        if result[0] != "OK":
            raise IMAPCommandException("UID MOVE", uid, dest)
