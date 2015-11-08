import os


class DockerParams:
    """
    [tr] default durumda, sistem hafizasinin yarisi, takasin tamami docker
    tarafindan kullanilabilir.

    islemci %50

    [en] In default, docker will use half of the system memory, and no limit
    on swap

    cpu %50
    """
    def __init__(self, params=None):
        self.system_memory, self.system_swap = self.memory()
        self.docker_memory = self.system_memory * 0.5
        self.docker_swap = -1
        self.cpu_bandwith = 1
        self.cpu_period = 400000
        self.cpu_quota = self.cpu_bandwith * self.cpu_period
        self.volumes = {}
        self.name = ''
        if params is not None:
            print(params)
            self.cpu_bandwith = params.cpu / 100
            self.cpu_quota = self.cpu_bandwith * self.cpu_period
            self.docker_memory = self.system_memory * params.memory / 100

    def set_name(self, new_name):
        import random
        temp = ''
        docker_name_allowed_characters = 'abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ-_1234567890'
        for c in new_name:
            if c not in docker_name_allowed_characters:
                c = docker_name_allowed_characters[random.randint(1, 50)]
            temp += c
        self.name = temp

    def set_memory(self, new_docker_memory, new_docker_swap):
        self.docker_memory = new_docker_memory
        self.docker_swap = new_docker_swap

    def volume(self, local, indocker):
        os.system("mkdir -p %s" % local)
        self.volumes[indocker] = local

    def volumes_str(self):
        temp = ""
        for ind, local in self.volumes.items():
            temp += " -v %s:%s " % (local, ind)
        return temp

    def mem_str(self):
        temp = ""
        if self.docker_swap > -1:
            temp = " --memory-swap %dM " % self.docker_swap
        if self.docker_memory > -1:
            temp += " -m %dM " % self.docker_memory
        return temp

    def cpu_str(self):
        return " --cpu-period=%d --cpu-quota=%d " % (self.cpu_period, self.cpu_quota)

    def name_str(self):
        if self.name == "":
            return ""
        else:
            return "--name %s-sil" % self.name

    def param_str(self, extra="", image=""):
        if self.name == "":
            return None
        return "%s %s %s %s %s %s " % (self.name_str(), self.cpu_str(), self.mem_str(),
                                       self.volumes_str(), image, extra)

    @staticmethod
    def memory():
        """
        [en] return physical and swap memory in megabytes
        [tr] fiziksel ve takas hafiza boyu, megabyte olarak
        """
        mem = int(os.popen("free -m | grep Mem").readlines()[0].split()[1])
        swp = int(os.popen("free -m | grep Swap").readlines()[0].split()[1])
        return mem, swp
