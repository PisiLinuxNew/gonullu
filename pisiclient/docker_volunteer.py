from pisiclient.docker import Docker


class DockerVolunteer(Docker):
    def __init__(self, params=None):
        Docker.__init__(self, params)
        self.params.volume('/var/cache/pisi/packages', '/var/cache/pisi/packages')
        self.params.volume('/var/cache/pisi/archives', '/var/cache/pisi/archives')
        self.params.volume('/tmp/build', '/build')
