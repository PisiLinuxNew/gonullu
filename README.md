# pisi-farm-gonullu
Pisilinux paket derleme sistemi icin gonullu uygulamasi



usage: gonullu.py [-h] [-k] [-j CPUCOUNT] [-e EMAIL] [-c CPU] [-m MEMORY]

This is pisilinux volunteer application

optional arguments:
  -h, --help            show this help message and exit
  -k, --kullanim        Kullanim. Usage
  -j CPUCOUNT, --make-j-num CPUCOUNT
                        make icin -j parametresine verilecek rakam. The number
                        for the make -j
  -e EMAIL, --email EMAIL
                        kuyruktan paket alirken gonderilecek olan mail adresi.
                        Email address of the volunteer.
  -c CPU, --cpu CPU     islemci kullanma yuzdesi. 1-100 arasi tamsayi. Cpu
                        limit for docker. A number between 1-100 as percent.
  -m MEMORY, --memory MEMORY
                        Hafiza kullanma yuzdesi. 1-100 arasi tamsayi. Memory
                        limit for docker. A number between 1-100 as percent of
                        total physical memory
