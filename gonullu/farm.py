import requests
import glob
import hashlib
import time


class Farm:
    def __init__(self, farm_url, email):
        self.url = farm_url
        self.email = self.mail_control(email)

    def get(self, request, json=True):
        # Get isteğini işleyip json data dönen fonksiyonumuz.
        if json:
            return requests.get('%s/%s' % (self.url, request)).json()
        else:
            return requests.get('%s/%s' % (self.url, request))

    def send_file(self, package):
        # Oluşan çıktı dosyalarını çiftliğe gönderen fonksiyonumuz.
        output_files = glob.glob('/tmp/gonullu/%s/*.[lpe]*' % package)
        for file in output_files:
            if self.send(file):
                pass
            else:
                while not (self.send(file)):
                    print('%s dosyasını yüklemeyi tekrar deniyoruz.' % file)
                    time.sleep(5)
        return True

    def send(self, file):
        print('%s Dosyası Gönderiliyor...' % file)
        if file.split('.')[-1] in ('err', 'log'):
            content = open(file, 'r').read()
            html = open('%s.html' % file, 'w')
            html.write('<html><body><pre>')
            html.write(content)
            html.write('</pre></body></html>')
            html.close()
        f = {'file': open('%s.%s' % (file, 'html'), 'rb')}
        r = requests.post('%s/%s' % (self.url, 'upload'), files=f)
        hashx = self.sha1file('%s.html' % file)
        print('>> Uzak sunucu hash: %s', r.text.strip())
        print('>> Yerel sunucu hash: %s', hashx)

        if hashx == r.text.strip():
            print('%s Dosyası Başarı ile Gönderildi...' % file)
            return True
        else:
            print('%s Dosyası Gönderilemedi Tekrar Denenicek!' % file)
            return False

    def get_package(self):
        request = '/%s/%s' % ('requestPkg', self.email)
        response = self.get(request)

        if response['state'] == 200:
            print('Paket bulundu.')
            return response

        elif response['state'] == 401:
            print('Mail adresi onaylı değildir.')
            return -1

        elif response['state'] == 402:
            print('Paket bulunamadı.')
            return -1

        elif response['state'] == 403:
            print('Docker imajı bulunamadı.')
            return -1

        else:
            print('Belirsiz bir hata oluştu.')
            return -1

    @staticmethod
    def mail_control(email):
        # Mail adresimiz onaylı mı diye kontrol eden fonksiyonumuz.
        # TODO: İlker abiden mail adresi onaylı mı diye istek yapabileceğimiz bir url isteyeceğiz.
        return email

    def running_process(self):
        # uygulama çalışmaya devam ettiği sürece siteye bildirim göndereceğiz.
        # TODO: İlker abiden devam ediyor olan uygulamalar kısmına bunun ile ilgili bir servis isteyeceğiz.
        pass

    def complete_process(self):
        # uygulama çalışması bitince çalışacak olan prosedür fonksiyonumuz.
        pass

    @staticmethod
    def sha1file(filepath):
        import hashlib
        sha = hashlib.sha1()
        with open(filepath, 'rb') as f:
            while True:
                block = f.read(2 ** 10)  # Magic number: one-megabyte blocks.
                if not block: break
                sha.update(block)
            return sha.hexdigest()
