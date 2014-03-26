import os


class VirtIOLogger(object):

    def write(self, data):
        virtio_port = "org.clouda.1"
        port = open(os.path.join("/dev/virtio-ports", virtio_port), "w")
        port.write(data)
        port.close()
