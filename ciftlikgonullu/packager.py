import os


class Packager:
    def __init__(self, dock, docker_image_name=None):
        self.docker = dock
        self.success = None
        self.docker_image_name = docker_image_name
        self.package = None
        self.kernel_requirement = None

    def set_package(self, new_package):
        self.package = new_package

    def is_running(self):
        cmd = "ls /tmp/%s/%s.bitti" % (self.package, self.package)
        status = os.system(cmd)
        if status == 0:
            self.success = int(open("/tmp/%s/%s.bitti" % (self.package, self.package), "r").readlines()[0])
        return status, self.success
