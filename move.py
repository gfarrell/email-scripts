import time

BATCH_SIZE=250
REST_TIME=100/1000 # 100µs

def batch_move(mailbox, uids, to):
    """executes the move command for batches of messages"""
    i = 0 # batch index number
    t = 0 # total done count
    total = len(uids)
    for uid in uids:
        mailbox.move_message(uid, to)
        i = (i + 1) % BATCH_SIZE
        t += 1
        if i == 0:
            mailbox.log("DONE {}/{} ({:.2%})", t, total, t/total)
            time.sleep(REST_TIME)

def cmd_move(mailbox, ffrom, to):
    """moves emails from one folder to another"""
    messages = mailbox.get_all_uids(ffrom)
    mailbox.log("MOVING MESSAGES {} ~> {}", ffrom, to)
    batch_move(mailbox, messages, to)
