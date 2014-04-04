import re
import signal
import sys

import gevent
from bricks_occupant import serialserver, util, seriallogger
from gevent.subprocess import Popen, PIPE


def monitor_workers():
    """
    Starts our serial server and ensures that it stays up.
    Also, looks for new Dockerfile dirs and processes them.
    """

    workers = []

    keep_processing = True

    while keep_processing:
        for w in workers:
            if w.returncode is not None:
                print "Alienating returned worker"
                workers.remove(w)

        if len(workers) < 1:
            print "Starting new worker"
            script_path = re.sub(r'c$', "", serialserver.__file__)
            sub = Popen(["python %s" % script_path],
                        stdout=PIPE, stderr=PIPE, shell=True)
            workers.append(sub)

        gevent.sleep(2)

    for w in workers:
        w.kill()


def periodic_tasks():
    """
    Runs our dockerfile scan every 15s
    """

    while True:
        try:
            docker_dirs = []
            print "Scanning for dockerfiles..."
            docker_dirs = util.find_docker_files()
            print "done."

            # Let's just process one dockerstack repo at a time
            if len(docker_dirs) > 0:
                print "Processing dockerfile"
                print "---%s" % docker_dirs[0]
                util.proc_docker_file(docker_dirs[0])
                print "done."
        except Exception as e:
            print e.message

        gevent.sleep(15)


def main():
    sys.stdout = seriallogger.VirtIOLogger()
    sys.stderr = seriallogger.VirtIOLogger()
    worker_thread = gevent.spawn(monitor_workers)
    periodic_task_thread = gevent.spawn(periodic_tasks)

    def stop(signal, frame):
        worker_thread.kill()
        periodic_task_thread.kill()
        sys.exit()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    gevent.joinall([worker_thread, periodic_task_thread])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
