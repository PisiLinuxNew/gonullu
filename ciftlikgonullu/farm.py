import os
import json
import requests
import time


class Farm:
    def __init__(self, farm_url):
        self.url = farm_url
        self.params = self.parametre()

    def get(self, cmd):
        return requests.get("%s/%s" % (self.url, cmd)).text

    def take_package_from_queue(self, email):
        cmd = "requestPkg/%s" % email
        return json.loads(self.get(cmd))

    def parametre(self):
        information = self.get("parameter")
        return json.loads(information)

    def docker_name(self, repo, branch):
        for r in self.params:
            if (r['repo'] == repo) and (r['branch'] == branch):
                return r['dockerimage']
        return None

    def send_file(self, fname, binpath):
        cmd = "upload"
        extension = ""
        if fname.split(".")[-1] in ("err", "log"):
            content = open(fname, "r").read()
            htm = open("%s.html" % fname, "w")
            htm.write("<html><body><pre>")
            htm.write(content)
            htm.write("</pre></body></html>")
            htm.close()
            extension = ".html"
        f = {'file': open("%s%s" % (fname, extension), 'rb')}
        r = requests.post("%s/%s" % (self.url, cmd), data = {'binrepopath':binpath}, files=f)
        hashx = os.popen("sha1sum %s%s" % (fname, extension), "r").readlines()[0].split()[0].strip()
        print(">> uzak hash   : %s" % r.text.strip())
        print(">> yakin hash  : %s" % hashx)

        if hashx == r.text.strip():
            return True
        else:
            return False

    def send_files(self, mylist, binpath):
        for f in mylist:
            print("dosya gonderiliyor, %s" % f)
            if self.send_file(f, binpath):
                print("%s gonderildi" % f)
            else:
                while not(self.send_file(f, binpath)):
                    print("%s deniyoruz" % f)
                    time.sleep(5)
        print(mylist)
