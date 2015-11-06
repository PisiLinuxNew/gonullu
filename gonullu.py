import urllib2
import os
import sys
import json
import glob
import time


try:
    import requests
except:
    print("Please install python-requests package.\nLutfen python-requests paketini yukleyin.")
    sys.exit()

try:
    import argparse
except:
    print("Please install python-argparse package.\nLutfen python-argparse paketini yukleyin.")
    sys.exit()


EMAIL = "ilkermanap@gmail.com"


docker_name_allowed_characters = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ-_1234567890"

def hazirlik(kernel_gerekli, j = 5):
    krn = " "
    if kernel_gerekli == True:
        krn = " kernel "
    derlesh = """#!/bin/bash
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

    gelistirsh = """#!/bin/bash
# birinci paket adi,
# ikinci pspec adresi
service dbus start && pisi cp && pisi ar pisi-2.0 http://ciftlik.pisilinux.org/pisi-2.0/pisi-index.xml.xz && pisi it --ignore-safety --ignore-dependency autoconf autogen automake binutils bison flex gawk gc gcc gnuconfig guile libmpc libtool-ltdl libtool lzo m4 make mpfr pkgconfig yacc glibc-devel %s
pisi ar core https://github.com/pisilinux/core/raw/master/pisi-index.xml.xz && pisi ar main https://github.com/pisilinux/main/raw/master/pisi-index.xml.xz --at 2
pisi ur
cd /root
pisi bi --ignore-safety -y $2 1>$1.log 2>$1.err
STAT=$?
echo $STAT >  $1.bitti
""" % krn
    os.system("mkdir -p /tmp/derle")
    f = open("/tmp/derle/derle.sh","w")
    f.write(derlesh)
    f.close()
    f = open("/tmp/derle/gelistirici.sh","w")
    f.write(gelistirsh)
    f.close()
    os.system("chmod 755 /tmp/derle/*.sh")


def hafiza():
    """
    [en] return physical and swap memory in megabytes
    [tr] fiziksel ve takas hafiza boyu, megabyte olarak
    """
    mem = int(os.popen("free -m | grep Mem").readlines()[0].split()[1])
    swp = int(os.popen("free -m | grep Swap").readlines()[0].split()[1])
    return mem, swp

def bekle(n, mesaj):
    times = n / 5
    for i in range(times):
        print("%s. Durdurmak icin CTRL-C'ye basiniz. %d sn kaldi." % (mesaj,(n -(i*5))))
        time.sleep(5)

class DockerParams:
    """
    [tr] default durumda, sistem hafizasinin yarisi, takasin tamami docker
    tarafindan kullanilabilir.

    islemci %50

    [en] In default, docker will use half of the system memory, and no limit
    on swap

    cpu %50,
    """

    def __init__(self, params = None):
        self.sistem_hafiza, self.sistem_takas = hafiza()
        self.docker_hafiza = self.sistem_hafiza * 0.5
        self.docker_takas = -1
        self.cpu_kota = 1
        self.cpu_period = 400000
        self.cpu_quota = self.cpu_kota * self.cpu_period
        self.volumes = {}
        self.name = ""
        if params is not None:
            print params
            self.cpu_kota = params.cpu / 100
            self.cpu_quota = self.cpu_kota * self.cpu_period
            self.docker_hafiza = self.sistem_takas * params.memory / 100

    def set_name(self, new_name):
        import random
        temp = ""
        for c in new_name:
            if c not in docker_name_allowed_characters:
                c = docker_name_allowed_characters[random.randint(1,50)]
            temp += c
        self.name = temp


    def set_hafiza(self, yeni_docker_hafiza, yeni_docker_takas):
        self.docker_hafiza = yeni_docker_hafiza
        self.docker_takas = yeni_docker_takas

    def set_cpu(self, yeni_cpu_orani):
        """
        [tr] yeni_cpu_orani 0 ile 1 arasinda float bir sayi olacaktir. 0 verilirse, en dusuk %10 yapilacaktir.
        [en] yeni_cpu_orani will be a float value between 0 and 1. If it is given less then %10, it will be %10.
        """
        if yeni_cpu_orani < 0.1:
            yeni_cpu_orani = 0.1
        if yeni_cpu_orani > 1:
            yeni_cpu_orani = 1
        self.cpu_kota = yeni_cpu_orani
        self.cpu_quota = self.cpu_kota * self.cpu_period

    def volume(self, local, indocker):
        self.volumes[indocker] = local

    def volumes_str(self):
        temp = ""
        for ind, local in self.volumes.items():
            temp += " -v %s:%s " % (local, ind)
        return temp

    def mem_str(self):
        temp = ""
        if self.docker_takas > -1:
            temp = " --memory-swap %dM " % self.docker_takas
        if self.docker_hafiza > -1:
            temp += " -m %dM " % self.docker_hafiza
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

class Docker:
    def __init__(self, params = None):
        self.started = self.start()
        self.image = ""
        self.id = None
        self.params = DockerParams(params)
        self.cpucount = params.cpucount
        self.params.volume('/tmp/derle', '/derle')

    def set_image_name(self, newname):
        self.image = newname
        self.retrieve()

    def retrieve(self):
        if self.image != "":
            if self.check() == 0:
                cmd = "docker pull %s" % self.image
                os.system(cmd)

    def rm(self, imgname):
        cmd = "docker rm %s" % imgname
        status = os.system(cmd)
        return status

    def check(self):
        cmd = "docker ps >/dev/null"
        status = os.system(cmd)
        return status

    def run(self, extra_params=""):
        prm = "docker run -id  %s " % (self.params.param_str(extra_params, self.image))
        print prm
        return prm

    def start(self):
        if self.check() != 0:
            print "Starting docker"
            cmd2 = "docker -d &"
            stat2 = os.system(cmd2)
            if stat2 == 0:
                return True
        else:
            print "Docker already started"
            return True
        return False


class DockerGonullu(Docker):
    def __init__(self, params = None):
        Docker.__init__(self, params)
        self.params.volume('/var/cache/pisi/packages', '/var/cache/pisi/packages')
        self.params.volume('/var/cache/pisi/archives', '/var/cache/pisi/archives')
        self.params.volume('/tmp/derle', '/derle')

class Paketci:
    def __init__(self, dock, docker_imaj_adi=None):
        self.docker = dock
        self.basari = None
        self.docker_imaj_adi = docker_imaj_adi
        self.paket = None
        self.kernel_gerekli = None

    def set_paket(self, yeni_paket):
        self.paket = yeni_paket

    def calisma_kontrol(self):
        cmd = "ls /tmp/%s/%s.bitti" % (self.paket, self.paket)
        status = os.system(cmd)
        if status == 0:
            self.basari = int(open("/tmp/%s/%s.bitti" % (self.paket, self.paket), "r").readlines()[0])
        return status, self.basari


class Gelistirici(Paketci):
    def __init__(self, dock):
        Paketci.__init__(self, dock)
        self.pspec = ""

    def set_pspec(self, pspec):
        self.pspec = pspec

    def farm_paket_al(self, email=EMAIL):
        d = self.farm.kuyruktan_paket_al(email)
        self.paket = d['paket']
        self.docker.params.set_name( self.paket)
        self.repo = d['repo']
        self.branch = d['branch']
        self.docker_imaj_adi = self.farm.docker_adi(d['repo'], d['branch'])
        self.docker.set_image_name(self.docker_imaj_adi)
        self.commit_id = d['commit_id']
        self.kuyruk_id = d['kuyruk_id']
        self.kernel_gerekli = d['kernel_gerekli']
        self.docker.params.volume('/tmp/%s' % self.paket, "/root")

    def derle(self):
        self.farm_paket_al()
        extra = "/derle/derle.sh %s %s %s" % (self.kuyruk_id, self.commit_id, self.paket)
        cmd = self.docker.run(extra)
        status = os.system(cmd)
        calisiyor = True
        while calisiyor:
            time.sleep(10)
            calisma, basari = self.calisma_kontrol()
            if calisma == 0:
                calisiyor = False
                time.sleep(5)
                cmd = "updaterunning?id=%s&state=%s" % (self.kuyruk_id, basari)
                self.farm.get(cmd)
                return
            print "hala calisiyor"


class Gonullu(Paketci):
    def __init__(self, farm, dock):
        Paketci.__init__(self, dock)
        self.farm = farm
        self.commit_id = None
        self.kuyruk_id = None
        self.repo = None
        self.branch = None
        self.derle()
        self.gonder()

    def farm_paket_al(self, email=EMAIL):
            d = self.farm.kuyruktan_paket_al(email)
            if d['durum'] == 'paket yok':
                bekleme = True
                n = 10
                while bekleme == True:
                    bekle(n, "Derlenecek paket yok")
                    d = self.farm.kuyruktan_paket_al(email)
                    if d['durum'] == 'ok':
                        bekleme = False
                    else:
                        n += 10
                        if n > 300:
                            n = 300

            if d['durum'] == "ok":
                self.paket = d['paket']
                self.docker.params.set_name(self.paket)
                self.docker.params.volume("/tmp/varpisi/%s" % self.paket, "/var/pisi")
                self.repo = d['repo']
                self.branch = d['branch']
                self.docker_imaj_adi = self.farm.docker_adi(d['repo'], d['branch'])
                self.docker.set_image_name(self.docker_imaj_adi)
                self.commit_id = d['commit_id']
                self.kernel_gerekli = d['kernel_gerekli']
                hazirlik(self.kernel_gerekli, self.docker.cpucount)
                self.kuyruk_id = d['kuyruk_id']
                self.docker.params.volume('/tmp/%s' % self.paket, "/root")

    def gonder(self):
        liste = glob.glob("/tmp/%s/*.[lpe]*" % self.paket)
        print liste
        self.farm.dosyalari_gonder(liste, self.repo, self.branch)
        if self.docker.rm("%s-sil" % self.docker.params.name) != 0:
            print "imaj silinemedi ", self.paket
        tmptemizle = "rm -rf /tmp/%s" % self.paket
        os.system(tmptemizle)

    def derle(self):
        self.farm_paket_al()
        extra = "/derle/derle.sh %s %s %s" % (self.kuyruk_id, self.commit_id, self.paket)
        cmd = self.docker.run(extra)
        status = os.system(cmd)
        calisiyor = True
        while calisiyor:
            time.sleep(10)
            calisma, basari = self.calisma_kontrol()
            if calisma == 0:
                calisiyor = False
                time.sleep(5)
                cmd = "updaterunning?id=%s&state=%s" % (self.kuyruk_id, basari)
                self.farm.get(cmd)
                return
            print "hala calisiyor"


class Farm:
    def __init__(self, farm_url):
        self.url = farm_url
        self.params = self.parametre()

    def get(self, cmd):
        return urllib2.urlopen("%s/%s" % (self.url, cmd)).read()

    def kuyruktan_paket_al(self, email):
        cmd = "requestPkg/%s" % email
        return json.loads(self.get(cmd))

    def parametre(self):
        bilgi = self.get("parameter")
        return json.loads(bilgi)

    def docker_adi(self, repo, branch):
        for r in self.params:
            if (r['repo'] == repo) and (r['branch'] == branch):
                return r['dockerimage']
        return None

    def dosya_gonder(self, fname, r, b):
        cmd = "upload"
        ek = ""
        if fname.split(".")[-1] in ("err","log"):
            icerik = open(fname,"r").read()
            htm = open("%s.html" % fname, "w")
            htm.write("<html><body><pre>")
            htm.write(icerik)
            htm.write("</pre></body></html>")
            htm.close()
            ek = ".html"
        f = {'file': open("%s%s" % (fname, ek) , 'rb')}
        r = requests.post("%s/%s" % (self.url, cmd), files=f)
        hashx = os.popen("sha1sum %s%s" % (fname, ek), "r").readlines()[0].split()[0].strip()
        print ">> uzak hash   : %s"  % r.text.strip()
        print ">> yakin hash  : %s"  % hashx

        if hashx == r.text.strip():
            return True
        else:
            return False

    def dosyalari_gonder(self, liste, repo, branch):
        for f in liste:
            print "dosya gonderiliyor, ", f
            if self.dosya_gonder(f, repo, branch):
                print f, " gonderildi"
            else:
                while not(self.dosya_gonder(f, repo, branch)):
                    print f, " deniyoruz"
                    time.sleep(5)
        print liste



def kullanim():
    print """
Kullanim - Usage

Asagidaki satir, docker icindeki /etc/pisi/pisi.conf icinde bulunan
-j parametresini verecegimiz rakam ile degistirir.
The command below replaces the -j parameter in the file in the  docker
image /etc/pisi/pisi.conf with the number given from command line.

sudo python gonullu.py -j 24


Asagidaki satir, docker icin islemcinin %70'ini, fiziksel hafizanin
%25'ini  ayirir.
The command below reserves %70 of cpu and %25 of physical memory for
docker.

sudo python gonullu.py --cpu=70 --memory=25

"""
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is pisilinux volunteer application')
    parser.add_argument('-k', '--kullanim', action="store_true", help="Kullanim. Usage")
    parser.add_argument('-j', '--make-j-num', action="store", dest="cpucount", default=5, type=int,
                        help="make icin -j parametresine verilecek rakam. The number for the make -j")
    parser.add_argument('-e','--email', action="store", dest="email", type=str,
                        help="kuyruktan paket alirken gonderilecek olan mail adresi. Email address of the volunteer.")
    parser.add_argument('-c','--cpu', action='store', dest='cpu',type=int, default=70,
                        help="islemci kullanma yuzdesi. 1-100 arasi tamsayi. Cpu limit for docker. A number between 1-100 as percent.")
    parser.add_argument('-m', '--memory', action='store', dest='memory',type=int, default=50,
                        help="Hafiza kullanma yuzdesi. 1-100 arasi tamsayi. Memory limit for docker. A number between 1-100 as percent of total physical memory")

    args = parser.parse_args()
    if args.kullanim:
        kullanim()


    d = DockerGonullu(args)
    f = Farm("http://ciftlik.pisilinux.org/ciftlik")
    #f = Farm("http://ciftlik.pisilinux.org:5000")
    while 1:
        g = Gonullu(f, d)
        bekle(15,"Yeni paket almadan once durdurmak icin CTRL-C")

