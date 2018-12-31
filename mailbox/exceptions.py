class IMAPException(Exception):
    """Base IMAP Exception class"""
    pass

class IMAPFolderException(IMAPException):
    """Unable to open a folder"""
    def __init__(self, folder):
        message = "Unable to open folder {}".format(folder)
        super().__init__(message)

class IMAPCommandException(IMAPException):
    """Generic problems with a command"""
    def __init__(self, command, *args):
        message = "Unable to execute {} with args {}".format(command, args)
        super().__init__(message)
