import dockerstack_agent
import io
import os
import re
from uuid import uuid4


TMP_DIR = "/tmp/dockerstack/"


class Serial(object):
    """
    A serial object used for receiving file data from Mortar etc.
    """

    path = None
    contents = None
    directory = None
    file_name = None

    def __init__(self, path='/dev/virtio-ports/org.clouda.0'):
        """
        Initialize socket connection
        """
        self.path = path
        self.directory = os.path.join(TMP_DIR, str(uuid4()))

    def read(self):
        """
        Receives our file from serial
        """
        serial = io.open(self.path)

        while True:
            try:
                line = serial.readline()

                #Stop reading if we've reached the end of the stream
                if re.match('StopStream\n', line):
                    break
                #Write our file if we've reached EOF and clear our buffer
                elif re.match('EOF\n', line):
                    self.write_contents()
                    self.contents = ""
                elif re.match(r'BOF [a-zA-Z0-9._-]+\n', line):
                    self.file_name = re.sub("\n", "", line[4:])
                    self.contents = ""
                #Generate a filename if invalid pattern or none given
                elif re.match('BOF', line):
                    self.file_name = str(uuid4())
                    self.contents = ""
                elif re.match('StartStream\n', line):
                    if not os.path.exists(self.directory):
                        os.makedirs(self.directory)
                    self.contents = ""
                else:
                    self.contents += serial.readline()
            except:
                break

    def get_contents(self):
        """
        Returns the contents of the file
        """
        return self.contents

    def write_contents(self):
        """
        Write contents to file
        """
        dfile = open(os.path.join(self.directory, self.file_name), "w")
        dfile.write(self.contents)


def find_docker_files():
    """
    Find docker files
    """
    os.chdir(TMP_DIR)
    docker_dirs = filter(os.path.isdir, os.listdir(TMP_DIR))
    docker_dirs = [os.path.join(TMP_DIR, d) for d in docker_dirs]
    docker_dirs.sort(key=lambda x: os.path.getmtime(x))

    return docker_dirs

def proc_docker_file(directory):
    """
    Process a dockerfile directory
    """
    dockerstack_agent.builder.do_build(directory)
