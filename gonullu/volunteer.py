import os

from gonullu.docker import Docker


class Volunteer(Docker):
    def __init__(self, params=None):
        Docker.__init__(self, params)
        self.package = None
        self.commit_id = None
        self.queue_id = None
        self.repo = None
        self.branch = None
        self.kernel_requirement = None

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
        self.queue_id = response['queue_id']
        self.preparation(self.kernel_requirement, self.package, self.cpu_set)
        self.set_command('/build/build-%s.sh' % self.package, self.queue_id, self.commit_id, self.package)
        self.start()

    @staticmethod
    def preparation(kernel_require, package, j=5):
        krn = ' '
        if kernel_require is True:
            krn = ' kernel '
        build_sh = """#!/bin/bash
service dbus start && pisi cp && pisi ar pisiBeta --ignore-check http://ciftlik.pisilinux.org/2.0-Beta/pisi-index.xml.xz && pisi it --ignore-safety --ignore-dependency autoconf autogen automake binutils bison flex gawk gc gcc gnuconfig guile libmpc libtool-ltdl libtool lzo m4 make mpfr pkgconfig yacc glibc-devel isl %s
pisi ar core --ignore-check https://github.com/pisilinux/core/raw/master/pisi-index.xml.xz && pisi ar main --ignore-check https://github.com/pisilinux/main/raw/master/pisi-index.xml.xz --at 2
pisi ur
sed -i 's/-j5/-j%d/g' /etc/pisi/pisi.conf
cd /root
pisi bi --ignore-safety --ignore-sandbox -y $3 1>/root/%s/$1-$2-$3.log 2>/root/%s/$1-$2-$3.err
STAT=$?
for s in `ls *.pisi`
do
    mv $s /root/%s/$1-$2-$s
done
echo $STAT >  /root/%s/$3.bitti
""" % (krn, j, package, package, package, package)

        build_directory = os.path.join('/tmp', 'gonullu', 'build')
        if not os.path.exists(build_directory):
            os.makedirs(build_directory)

        f = open(os.path.join(build_directory, 'build-%s.sh' % package), 'w')
        f.write(build_sh)
        f.close()
        os.chmod(os.path.join(build_directory, 'build-%s.sh' % package), 0o755)
