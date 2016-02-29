# Gonullu uygulamasi

Gonullu uygulamasi, pisi linux dagitiminin paketlerini derlemek uzere hazirlanmistir.
Uygulama, docker imajlari kullanarak, derleme sisteminin kuyrugunda bekleyen paketleri
pisi paketi haline getirir ve derleme sistemine gonderir.

Bu uygulamayi kullanmak icin pisi linux kullanmaniz sart degildir. Docker destekleyen
herhangi bir linux dagitiminda da calisabilir.

## Kullanim

Uygulamayi sisteminize indirmek icin

  	   git clone https://github.com/PisiLinuxNew/gonullu
  	   cd gonullu
  	   sudo python3 setup.py install
  	   
ya da

  	   sudo pip3 install git+https://github.com/PisiLinuxNew/gonullu.git
  	   
Uygulamayı güncellemek için

  	   sudo pip3 install git+https://github.com/PisiLinuxNew/gonullu.git --upgrade

Uygulamaya verilebilecek parametreleri gormek icin:

  	   gonullu -h

ya da

	   gonullu --help

Parametre vermeden kullanirsaniz, islemcinin %70'ini, hafizanin %50'sini kullanacak sekilde
ayarlanmistir. 
