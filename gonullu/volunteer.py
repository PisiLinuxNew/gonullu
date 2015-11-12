from gonullu.docker import Docker


class Volunteer(Docker):
    def __init__(self, params=None):
        # Docker sınıfımızı initialize edelim.
        Docker.__init__(self, parameters=params)
