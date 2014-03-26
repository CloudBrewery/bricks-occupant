import re
import sys

import gevent
from bricks_occupant import serialserver, util
from gevent.subprocess import Popen, PIPE


def monitor_workers():
    """
    Starts our serial server and ensures that it stays up.
    Also, looks for new Dockerfile dirs and processes them.
    """

    workers = []
    while True:
        for w in workers:
            if w.returncode is not None:
                workers.remove(w)

        if len(workers) < 1:
            script_path = re.sub(r'c$', "", serialserver.__file__)
            sub = Popen(["python %s" % script_path],
                        stdout=PIPE, shell=True)
            workers.append(sub)
        gevent.sleep(1)


def main():
    thread = gevent.spawn(monitor_workers)
    thread.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)

