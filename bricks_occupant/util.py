import io
import re
from uuid import uuid4


class Serial(object):
    """
    A serial object used for receiving file data from Mortar etc.
    """

    path = None
    contents = None
    file_name = None

    def __init__(self, path='/dev/virtio-ports/org.clouda.0'):
        """
        Initialize socket connection
        """
        self.path = path
        self.file_name = uuid4()

    def read(self):
        """
        Receives our file from serial
        """
        serial = io.open(self.path)

        while True:
            try:
                line = serial.readline()

                #Stop reading if we've reached the end of the file
                if re.match('EOF\n', line):
                    break
                elif re.match('BOF\n', line):
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
        dfile = open('/tmp/dockerstack/%s' % self.file_name, 'w')
        dfile.write(self.contents)
