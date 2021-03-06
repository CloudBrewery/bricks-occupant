import io
import os
import re
import time
import traceback

from shutil import rmtree
from uuid import uuid4

import dockerstack_agent.builder


TMP_DIR = '/tmp/dockerstack/'
SERIAL_PATH = '/dev/virtio-ports/org.clouda.0'


class Serial(object):

    """A serial object used for receiving file data from Mortar etc.
    """

    def __init__(self, path=SERIAL_PATH):
        """Initialize socket connection.
        """
        self.contents = ''
        self.file_name = None

        self.path = path
        self.directory = os.path.join(TMP_DIR, str(uuid4()) + '_working')

    def read(self):
        """Receives files from serial port
        """

        serial = io.open(self.path)

        on_line = False

        while True:
            try:
                line = serial.readline()
                on_line = line != ''

                #Stop reading if we've reached the end of the stream and mark
                #directory as ready
                if re.match(r'(\n*)StopStream\n', line):
                    os.rename(self.directory, self.directory[:-8])
                    print "Done stream."
                    break
                #Write our file if we've reached EOF and clear our buffer
                elif re.match(r'(\n*)EOF\n', line):
                    print "Done creating file."
                    self.write_contents()
                    self.contents = ''
                elif re.match(r'(\n*)BOF [a-zA-Z0-9._-]+\n', line):
                    self.file_name = re.sub('\n', '', line[4:])
                    print "Creating file %s" % self.file_name
                    self.contents = ''
                #Generate a filename if invalid pattern or none given
                elif re.match(r'(\n*)BOF', line):
                    print "Creating file with random name..."
                    self.file_name = str(uuid4())
                    self.contents = ''
                elif re.match(r'(\n*)StartStream\n', line):
                    print "Streaming...."
                    if not os.path.exists(self.directory):
                        print "Creating directory %s" % self.directory
                        os.makedirs(self.directory)
                    self.contents = ''
                else:
                    self.contents += line

                if not on_line:
                    time.sleep(2)
            except:
                pass

    def get_contents(self):
        """Returns the contents of the file.
        """
        return self.contents

    def write_contents(self):
        """
        Write contents to file
        """
        dfile = open(os.path.join(self.directory, self.file_name), 'w')
        dfile.write(self.contents.strip())


def find_docker_files():
    """Finds docker files in the working tmp dir.
    """
    docker_dirs = []
    if os.path.exists(TMP_DIR):
        docker_dirs = [os.path.join(TMP_DIR, d) for d in os.listdir(TMP_DIR)
                       if os.path.isdir(os.path.join(TMP_DIR, d)) and
                       not d.endswith('_working')]
        docker_dirs.sort(key=lambda x: os.path.getmtime(x))

    return docker_dirs


def proc_docker_file(directory):
    """Process a dockerfile directory.

    :param directory: The target directory for dockerstack agent.
    """
    print "TASK-RUNNING"
    os.rename(directory, directory + '_working')
    directory += '_working'
    try:
        dockerstack_agent.builder.do_build(directory)
        rmtree(directory)
    except Exception as e:
        traceback.print_exc()
        print "TASK-ERROR"
        raise e
    #finally:
        #Remove the directory

    print "TASK-COMPLETE"
