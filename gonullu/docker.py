import random

from docker import Client
import psutil


class Docker:
    def __init__(self, parameters=None):
        self.name = self.set_name(parameters.name)
        self.memory_limit = self.set_memory_limit(parameters.memory_limit)
        self.memswap_limit = self.set_memswap_limit(parameters.memswap_limit)
        self.volumes = self.set_volumes(parameters.volumes)
        self.image = self.set_image(parameters.image)
        self.cpu_shares = self.set_cpu_shares(parameters.cpu_shares)
        self.cpu_set = self.set_cpu_set(parameters.cpu_set)
        self.command = self.set_command(parameters.command)
        self.my_client = None
        self.my_container = None

    def start(self):
        # containerımızı parametreleri ile çalıştıracağımız fonksiyonumuz.
        # my_client'de çalışan docker process'ini yakalıyorum.
        self.my_client = Client(base_url='unix://var/run/docker.sock')
        # create_host_config ile limitlerimizi atıyoruz.
        self.my_client.create_host_config(mem_limit=self.memory_limit, memswap_limit=self.memswap_limit,
                                          volumes=self.volumes)
        # my_container ile konteynırımızı oluşturuyoruz ve onda saklıyoruz.
        self.my_container = self.my_client.create_container(image=self.image, cpu_shares=self.cpu_shares,
                                                            cpuset=self.cpu_set, command=self.command, name=self.name)
        # ve konteynırımızı çalıştırmaya başlıyoruz.
        self.my_client.start(self.name)

    def pause(self):
        # containerımızı durdurmak için çalıştıracağımız fonksiyonumuz.
        self.my_client.pause(self.name)

    def resume(self):
        # containerımızı devam ettirmek için çalıştıracağımız fonksiyonumuz.
        self.my_client.unpause(self.name)

    def stop(self):
        # konteynırımızda ki işlemi iptal etmek için çalıştıracağımız fonksiyonumuz.
        self.my_client.stop(self.name)

    def remove(self):
        # containerımızı silecek fonksiyonumuz
        self.my_client.remove_container(self.name)

    def get_logs(self):
        # burada oluşan log çıktılarımızı yakalayacağız.
        self.my_client.logs(self.name)

    @staticmethod
    def set_name(name):
        # container adımızı atadığımız fonksiyonumuz.
        dictionary = 'abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ-_1234567890'
        dictionary_len = len(dictionary)
        new_name = None
        for i in name:
            if i not in dictionary:
                i = dictionary[random.randint(1, dictionary_len)]
            new_name += i

        return new_name

    @staticmethod
    def set_memory_limit(memory_limit):
        # ram limitimizi atadığımız fonksiyonumuz.
        return int((psutil.virtual_memory().total * (memory_limit / 100))) >> 20

    @staticmethod
    def set_memswap_limit(memswap_limit):
        # swap limitimizi atadığımız fonksiyonumuz.
        return int((psutil.swap_memory().total * (memswap_limit / 100))) >> 20

    @staticmethod
    def set_image(image):
        # imajımızı atadığımız fonksiyonumuz.
        return image

    @staticmethod
    def set_cpu_shares(cpu_shares):
        # paylaşılan cpularımızı atadığımız fonksiyonumuz.
        return cpu_shares

    @staticmethod
    def set_cpu_set(cpu_set):
        # atayacağımız cpularımızı atadığımız fonksiyonumuz.
        return cpu_set

    @staticmethod
    def set_volumes(volumes):
        # bölümleri atadığımız fonksiyonumuz.
        return volumes

    @staticmethod
    def set_command(command):
        # çalıştıracağımız komutu atadığımız fonksiyonumuz.
        return "%s %s %s %s" % (command.application, command.queue_id, command.commit_id, command.package)
