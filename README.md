# Gonullu uygulamasi

Gonullu uygulamasi, pisi linux dağıtımının paketlerini derlemek üzere hazırlanmıştır.
Uygulama, docker imajlarını kullanarak, derleme sisteminin kuyruğundan bekleyen paketleri
pisi paketi haline getirir ve derleme sistemine gönderir.

Bu uygulamayi kullanmak için pisi linux kullanmaniz şart değildir. Docker destekleyen
herhangi bir linux dağıtımınıda da kullanıyor olabilirsiniz.

## Kullanim

Uygulamayı sisteminize indirmek için

  	   git clone https://github.com/PisiLinuxNew/gonullu
  	   cd gonullu
  	   sudo python3 setup.py install
  	   
ya da

  	   sudo pip3 install git+https://github.com/PisiLinuxNew/gonullu.git
  	   
Uygulamayı güncellemek için

  	   sudo pip3 install git+https://github.com/PisiLinuxNew/gonullu.git --upgrade

Uygulamaya verilebilecek parametreleri gormek icin:

  	   gonullu -k

ya da

	   gonullu --kullanim

Parametre vermeden kullanirsaniz, islemcinin %70'ini, hafizanin %50'sini kullanacak sekilde
ayarlanmistir. 

## Parametreler

