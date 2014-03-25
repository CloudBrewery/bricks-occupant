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
            sub = Popen(['python serialserver.py'], stdout=PIPE, shell=True)
            workers.append(sub)
        gevent.sleep(1)


def main():
    gevent.spawn(monitor_workers)

if __name__ == '__main__':
    main()
