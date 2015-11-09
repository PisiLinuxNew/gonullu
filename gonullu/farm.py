import requests


class Farm:
    def __init__(self):
        self.url = ''

    def get(self, request):
        # Get isteğini işleyip json data dönen fonksiyonumuz.
        return requests.get('%s/%s' % (self.url, request)).json()

    def post(self, request, data):
        # Post isteğini işleyip json data dönen fonksiyonumuz.
        return requests.post('%s/%s' % (self.url, request), params=data).json()

    def take_package(self):
        # Kuyruktan paket alma fonksiyonumuz.
        pass

    def mail_control(self):
        # Mail adresimiz onaylı mı diye kontrol eden fonksiyonumuz.
        # TODO: İlker abiden mail adresi onaylı mı diye istek yapabileceğimiz bir url isteyeceğiz.
        pass

    def send_file(self):
        # Oluşan çıktı dosyalarını çiftliğe gönderen fonksiyonumuz.
        pass

    def running_process(self):
        # uygulama çalışmaya devam ettiği sürece siteye bildirim göndereceğiz.
        # TODO: İlker abiden devam ediyor olan uygulamalar kısmına bunun ile ilgili bir servis isteyeceğiz.
        pass

    def complete_process(self):
        # uygulama çalışması bitince çalışacak olan prosedür fonksiyonumuz.
        pass

    def get_image(self):
        # docker imajını öğreneceğimiz fonksiyonumuz.
        pass
