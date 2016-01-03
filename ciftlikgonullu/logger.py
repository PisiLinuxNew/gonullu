import subprocess
import os
import glob

class Logger:
    def __init__(self, package_name):
        self.package = package_name
        self.err_logs = []
        self.build_logs = []


    def read_files(self):
        errfile = ""
        buildfile = ""
        try:
            errfile = glob.glob('/tmp/%s/*.err' % self.package)[0]
        except:
            errfile = None

        try:
            buildfile = glob.glob('/tmp/%s/*.log' % self.package)[0]
        except:
            buildfile = None
        if errfile is not None:
            self.err_logs = self.read_log(errfile)

        if buildfile is not None:
            self.build_logs = self.read_log(buildfile)



    def read_log(self, name, numlines=10):
        #FIXME: Until finding out a better way to tail a file, I'll use subprocess
        if os.path.isfile(name) == True:
            f = subprocess.Popen(['tail', '-%d' % numlines, name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return f.stdout.readlines()
        else:
            return []

