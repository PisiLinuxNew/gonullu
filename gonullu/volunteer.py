import os
import yaml

from gonullu.docker import Docker
from gonullu.log import Log


class Volunteer(Docker):
    def __init__(self, params=None):
        Docker.__init__(self, params)
        self.log = Log()
        self.package = None
        self.commit_id = None
        self.queue_id = None
        self.repo = None
        self.branch = None
        self.kernel_requirement = None
        self.job = params.job

    def get_package_farm(self, response):
        self.package = response['package']
        self.set_name(self.package)
        self.add_volume('/var/cache/pisi/packages', '/var/cache/pisi/packages')
        self.add_volume('/var/cache/pisi/archives', '/var/cache/pisi/archives')
        self.add_volume('/tmp/gonullu/build', '/build')
        self.add_volume('/tmp/varpisi/%s' % self.package, '/var/pisi')
        self.add_volume('/tmp/gonullu/%s' % self.package, '/root/%s' % self.package)
        self.repo = response['repo']
        self.branch = response['branch']
        self.set_image(response['dockerimage'])
        self.commit_id = response['commit_id']
        self.kernel_requirement = response['kernel_required']
        self.sandbox_requirement = self.sandbox_is_require()
        self.queue_id = response['queue_id']
        self.preparation(self.kernel_requirement, self.sandbox_requirement, self.package, self.job)
        self.set_command('/build/build-%s.sh' % self.package, self.queue_id, self.commit_id, self.package)
        self.start()

    def sandbox_is_require(self):
        config_file = os.path.join(os.path.dirname(__file__), 'config/sandbox-requirement.yml')

        with open(config_file, 'r') as sandbox_file:
            try:
                #FIXME! yaml.load(input) is depricated
                if self.package in yaml.load(sandbox_file, Loader=yaml.FullLoader):
                    return False
            except:
                self.log.error(message='%s dosyası işlenemedi' % config_file)
                self.log.get_exit()

        return True

    @staticmethod
    def preparation(kernel_require, sandbox_requirement, package, j=5):
        krn = ' '
        sandbox = ' '
        if kernel_require is True:
            krn = ' kernel '

        if sandbox_requirement is False:
            sandbox = ' --ignore-sandbox '

        build_sh = """#!/bin/bash
service dbus start && pisi cp && update-ca-certificates && pisi ar pisiBeta https://ciftlik.pisilinux.org/2.0-Beta.1/pisi-index.xml.xz && pisi it --ignore-safety --ignore-dependency autoconf autogen automake binutils bison flex gawk gc gcc gnuconfig guile libmpc libsigsegv libtool-ltdl libtool lzo m4 make mpfr nasm pkgconfig yacc glibc-devel isl %s
pisi ar core --ignore-check https://github.com/pisilinux/core/raw/master/pisi-index.xml.xz && pisi ar main --ignore-check https://github.com/pisilinux/main/raw/master/pisi-index.xml.xz --at 2
pisi ur
sed -i 's/-j5/-j%d/g' /etc/pisi/pisi.conf
sed -i 's/build_host = localhost/build_host=farmV4/g'   /etc/pisi/pisi.conf
cd /root
pisi bi --ignore-safety%s-y $3 1>/root/%s/$1-$2-$3.log 2>/root/%s/$1-$2-$3.err
STAT=$?
for s in `ls *.pisi`
do
    mv $s /root/%s/$1-$2-$s
done
echo $STAT >  /root/%s/$3.bitti
""" % (krn, j, sandbox, package, package, package, package)

        build_directory = os.path.join('/', 'tmp', 'gonullu', 'build')
        if not os.path.exists(build_directory):
            os.makedirs(build_directory)

        f = open(os.path.join(build_directory, 'build-%s.sh' % package), 'w')
        f.write(build_sh)
        f.close()
        os.chmod(os.path.join(build_directory, 'build-%s.sh' % package), 0o755)
