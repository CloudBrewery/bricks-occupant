import sys

import bricks_occupant
import gevent
from gevent.subprocess import Popen, PIPE


def monitor_workers():
    """
    Starts our serial server and ensures that it stays up
    """

    workers = []
    while True:
        for w in workers:
            if w.returncode is not None:
                workers.remove(w)

        if len(workers) < 1:
            working_dir = bricks_occupant.__path__
            sub = Popen(['python %s/serialserver.py' % working_dir],
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

