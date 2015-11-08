from ciftlikgonullu.docker_params import DockerParams
import os


class Docker:
    def __init__(self, params=None):
        self.started = self.start()
        self.image = ''
        self.id = None
        self.params = DockerParams(params)
        self.cpucount = params.cpucount
        self.params.volume('/tmp/build', '/build')

    def set_image_name(self, newname):
        self.image = newname
        self.retrieve()

    def retrieve(self):
        if self.image != '':
            if self.check() == 0:
                cmd = "docker pull %s" % self.image
                os.system(cmd)

    def run(self, extra_params=""):
        prm = "docker run -id  %s " % (self.params.param_str(extra_params, self.image))
        print(prm)
        return prm

    def start(self):
        if self.check() != 0:
            print("Starting docker")
            cmd2 = "docker daemon -s overlay &"
            stat2 = os.system(cmd2)
            if stat2 == 0:
                return True
        else:
            print("Docker already started")
            return True
        return False

    @staticmethod
    def rm(imgname):
        cmd = "docker rm %s" % imgname
        status = os.system(cmd)
        return status

    @staticmethod
    def check():
        cmd = "docker ps >/dev/null"
        status = os.system(cmd)
        return status
