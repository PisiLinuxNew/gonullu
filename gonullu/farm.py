import glob
import time

import requests

from gonullu.log import Log


class Farm:
    def __init__(self, farm_url, email):
        self.url = farm_url
        self.email = self.mail_control(email)
        self.time = 10
        self.total_error_time = 10
        self.log = Log()
        self.total_time = 10

    def get(self, request, json=True):
        # Get isteğini işleyip json data dönen fonksiyonumuz.
        try:
            response = requests.get('%s/%s' % (self.url, request))
            if json:
                self.total_error_time = 10
                return response.json()
            else:
                self.total_error_time = 10
                return response
        except requests.ConnectionError:
            self.log.error('Sunucuya %s saniyedir erişilemedi tekrar bağlanmaya çalışıyor!' % self.total_error_time,
                           continued=True)
            self.total_error_time += 10
            self.total_time = 10
            return -2

    def send_file(self, package, binary_path):
        # Oluşan çıktı dosyalarını çiftliğe gönderen fonksiyonumuz.
        output_files = glob.glob('/tmp/gonullu/%s/*.[lpe]*' % package)
        for file in output_files:
            if self.send(file, binary_path):
                pass
            else:
                while not (self.send(file, binary_path)):
                    self.log.warning(message='%s dosyası tekrar gönderilmeye çalışılacak.' % file)
                    self.wait()
        return True

    def send(self, file, binary_path):
        self.log.information(message='%s dosyası gönderiliyor.' % file.split('/')[-1])
        if file.split('.')[-1] in ('err', 'log'):
            content = open(file, 'r').read()
            html = open('%s.html' % file, 'w')
            html.write('<html><body><pre>')
            html.write(content)
            html.write('</pre></body></html>')
            html.close()
            file = '%s.html' % file

        f = {'file': open(file, 'rb')}
        try:
            r = requests.post('%s/%s' % (self.url, 'upload'), files=f, data={'binrepopath': binary_path})
            hashx = self.sha1file(file)

            file = file.split('/')[-1]
            if hashx == r.text.strip():
                self.log.success(message='%s dosyası başarı ile gönderildi.' % file)
                return True
            else:
                self.log.error(message='%s dosyası gönderilemedi!' % file)
                return False
        except requests.ConnectionError:
            self.log.error(message='%s dosyası gönderilemedi!' % file)
            return False

    def get_package(self):
        request = '%s/%s' % ('requestPkg', self.email)
        response = self.get(request)

        if response == -1:
            return -1

        if response == -2:
            time.sleep(self.time)
            self.total_time += self.time
            return -2

        elif response['state'] == 200:
            self.log.information(message='Yeni paket bulundu, paketin adı: %s' % response['package'])
            self.total_time = 0
            return response

        elif response['state'] == 401:
            self.log.error(message='Mail adresiniz yetkili değil!')
            self.log.get_exit()

        elif response['state'] == 402:
            return -1

        elif response['state'] == 403:
            self.log.error(message='Docker imajı bulunamadı!')
            self.log.get_exit()

        else:
            self.log.error(message='Tanımlı olmayan bir hata oluştu!')
            self.log.get_exit()

    def wait(self, message='', reset=False):
        if reset is True:
            self.total_time = 0

        if not message == '':
            information_message = '%d saniye%s' % (self.total_time, message)
            self.log.information(message=information_message, continued=True)
        time.sleep(self.time)
        self.total_time += self.time

    def get_total_time(self):
        return self.total_time

    def running_process(self):
        # uygulama çalışmaya devam ettiği sürece siteye bildirim göndereceğiz.
        # TODO: İlker abiden devam ediyor olan uygulamalar kısmına bunun ile ilgili bir servis isteyeceğiz.
        pass

    def complete_process(self):
        # uygulama çalışması bitince çalışacak olan prosedür fonksiyonumuz.
        pass

    @staticmethod
    def mail_control(email):
        # Mail adresimiz onaylı mı diye kontrol eden fonksiyonumuz.
        # TODO: İlker abiden mail adresi onaylı mı diye istek yapabileceğimiz bir url isteyeceğiz.
        return email

    @staticmethod
    def sha1file(filepath):
        import hashlib
        sha = hashlib.sha1()
        with open(filepath, 'rb') as f:
            while True:
                block = f.read(2 ** 10)  # Magic number: one-megabyte blocks.
                if not block:
                    break
                sha.update(block)
            return sha.hexdigest()
