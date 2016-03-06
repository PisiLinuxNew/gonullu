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

Parametre vermeden kullanırsanız 1 adet cpu ve hafızanın %50'sini kullanacak şekilde ayarlanmistir. 

## Parametreler

* -k veya --kullanim:
Yazılımın kullanımı ile ilgili bilgi içerir

* -ml veya --memory-limit:
Docker tarafından kullanılacak fiziksel ramin limiti

* -msl veya --memory-swap-limit:
Docker tarafından kullanılacak swap alanı limiti

* -cs veya --cpu-set:
Docker tarafından kullanılmak üzere ayarlanacak cpu sayısı

* -e veya --email:
Mail adresiniz