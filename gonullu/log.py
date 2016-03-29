from colorama import init, Fore, Style
import sys
import os


class Log:
    def __init__(self):
        init(autoreset=True)
        self.new_line = False
        self.last_output_type = ''

    def error(self, message, continued=False):
        # burada hata mesajlarımızı yazdıracağız.
        if continued is True:
            if self.last_output_type != 'error':
                self.blank_line()
            print(Fore.RED + '  [x] Hata: ' + message + Style.RESET_ALL, end="\r")
            self.last_output_type = 'error'
            self.new_line = True
        else:
            if self.new_line is True:
                self.blank_line()
            print(Fore.RED + '  [x] Hata: ' + message + Style.RESET_ALL)
            self.new_line = False

    def information(self, message, continued=False):
        # burada bilgi mesajlarımızı yazdıracağız.
        if continued is True:
            if self.last_output_type != 'information':
                self.blank_line()
            print(Fore.LIGHTBLUE_EX + '  [*] Bilgi: ' + message + Style.RESET_ALL, end="\r")
            self.last_output_type = 'information'
            self.new_line = True
        else:
            self.new_line = False
            print(Fore.LIGHTBLUE_EX + '  [*] Bilgi: ' + message + Style.RESET_ALL)

    def success(self, message):
        # burada başlarılı işlem mesajlarımızı yazdıracağız.
        if self.new_line is True:
            self.blank_line()
        print(Fore.GREEN + '  [+] Başarılı: ' + message + Style.RESET_ALL)

    def warning(self, message, continued=False):
        # burada uyarı mesajlarımız olacak.
        if continued is True:
            if self.last_output_type != 'warning':
                self.blank_line()
            print(Fore.LIGHTBLUE_EX + '  [!] Uyarı: ' + message + Style.RESET_ALL, end="\r")
            self.last_output_type = 'warning'
        else:
            if self.new_line is True:
                self.blank_line()
            print(Fore.YELLOW + '  [!] Uyarı: ' + message + Style.RESET_ALL)

    @staticmethod
    def get_exit():
        sys.exit()

    def blank_line(self):
        self.new_line = False
        print('')
