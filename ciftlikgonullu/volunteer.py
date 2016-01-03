import glob
import os
import time

from ciftlikgonullu.packager import Packager
from ciftlikgonullu.logger import Logger

class Volunteer(Packager):
    def __init__(self, farm, dock):
        Packager.__init__(self, dock)
        self.farm = farm
        self.commit_id = None
        self.queue_id = None
        self.repo = None
        self.branch = None
        self.build()
        self.send()
        self.logger = None

    def take_package_farm(self, email='ilkermanap@gmail.com'):
        d = self.farm.take_package_from_queue(email)
        n = 10
        while d['durum'] == 'paket yok':
            self.wait(n, "Derlenecek paket yok")
            n += 10
            if n > 300:
                n = 300
            d = self.farm.take_package_from_queue(email)

        if d['durum'] == "ok":
            self.package = d['paket']
            self.logger = Logger(self.package)
            self.docker.params.set_name(self.package)
            self.docker.params.volume("/tmp/varpisi/%s" % self.package, "/var/pisi")
            self.repo = d['repo']
            self.branch = d['branch']
            self.docker_image_name = self.farm.docker_name(d['repo'], d['branch'])
            self.docker.set_image_name(self.docker_image_name)
            self.commit_id = d['commit_id']
            self.kernel_requirement = d['kernel_gerekli']
            self.preparation(self.kernel_requirement, self.docker.cpucount)
            self.queue_id = d['kuyruk_id']
            self.docker.params.volume('/tmp/%s' % self.package, "/root")

    def send(self):
        liste = glob.glob("/tmp/%s/*.[lpe]*" % self.package)
        print(liste)
        self.farm.send_files(liste)
        if self.docker.rm("%s-sil" % self.docker.params.name) != 0:
            print("imaj silinemedi %s" % self.package)
        tmptemizle = "rm -rf /tmp/%s" % self.package
        os.system(tmptemizle)

    def build(self):
        self.take_package_farm()
        extra = "/build/build.sh %s %s %s" % (self.queue_id, self.commit_id, self.package)
        cmd = self.docker.run(extra)
        os.system(cmd)
        i = 0
        while True:
            i += 1
            if (i % 12) == 0: # in every two minute, send the build and error log files to farm


            time.sleep(10)
            run, success = self.is_running()
            if run == 0:
                time.sleep(5)
                cmd = "updaterunning?id=%s&state=%s" % (self.queue_id, success)
                self.farm.get(cmd)
                return
            print("hala çalışıyor")

    @staticmethod
    def wait(n, mesaj):
        times = int(n / 5)
        for i in range(times):
            print("%s. Durdurmak icin CTRL-C'ye basiniz. %d sn kaldi." % (mesaj, (n - (i * 5))))
            time.sleep(5)
        return

    @staticmethod
    def preparation(kernel_require, j=5):
        krn = ' '
        if kernel_require is True:
            krn = ' kernel '
        build_sh = """#!/bin/bash
service dbus start && pisi cp && pisi ar pisi-2.0 http://ciftlik.pisilinux.org/pisi-2.0/pisi-index.xml.xz && pisi it --ignore-safety --ignore-dependency autoconf autogen automake binutils bison flex gawk gc gcc gnuconfig guile libmpc libtool-ltdl libtool lzo m4 make mpfr pkgconfig yacc glibc-devel %s
pisi ar core https://github.com/pisilinux/core/raw/master/pisi-index.xml.xz && pisi ar main https://github.com/pisilinux/main/raw/master/pisi-index.xml.xz --at 2
pisi ur
sed -i 's/-j5/-j%d/g' /etc/pisi/pisi.conf
cd /root
pisi bi --ignore-safety --ignore-sandbox -y $3 1>$1-$2-$3.log 2>$1-$2-$3.err
STAT=$?
for s in `ls *.pisi`
do
    mv $s $1-$2-$s
done
echo $STAT >  $3.bitti
""" % (krn, j)

        os.system("mkdir -p /tmp/build")
        f = open("/tmp/build/build.sh", "w")
        f.write(build_sh)
        f.close()
        os.system("chmod 755 /tmp/build/*.sh")
