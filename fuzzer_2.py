import requests
import sys
import os
from colorama import Fore, init
import argparse
from multiprocessing import Pool
import base64
import urllib.parse as urlparse
import re

init(autoreset=True)

DOMAIN = ""
DIRS = []
COUNT = 1


def greetings():
    """Функция отображает приветствие пользователя"""
    print(Fore.GREEN + '''
╔═══╗╔══╗╔═══╗     ╔═══╗╔╗─╔╗╔════╗╔════╗╔═══╗╔═══╗
╚╗╔╗║╚╣║╝║╔═╗║     ║╔══╝║║─║║╚══╗═║╚══╗═║║╔══╝║╔═╗║
─║║║║─║║─║╚═╝║     ║╚══╗║║─║║──╔╝╔╝──╔╝╔╝║╚══╗║╚═╝║
─║║║║─║║─║╔╗╔╝     ║╔══╝║║─║║─╔╝╔╝──╔╝╔╝─║╔══╝║╔╗╔╝
╔╝╚╝║╔╣║╗║║║╚╗     ║║───║╚═╝║╔╝═╚═╗╔╝═╚═╗║╚══╗║║║╚╗
╚═══╝╚══╝╚╝╚═╝     ╚╝───╚═══╝╚════╝╚════╝╚═══╝╚╝╚═╝
          ''')


def check_wordlist_file(path_to_wordlist):
    """Функция проверяет наличие файла со словарём"""
    if not os.path.isfile(path_to_wordlist.replace("\'", "")):
        print(f"{path_to_wordlist}\nФайл со словарём не найден.")
        sys.exit(0)
    fill_dirs_from_file(path_to_wordlist)


def set_url_format(hostname):
    """Функция проверяет форматирование url сайта"""
    global DOMAIN
    if hostname[-1] != "/":
        hostname += "/"
    else:
        DOMAIN = hostname


def check_app_keys():
    """Функция проверяет правильность аргументов"""
    # Количество аргументов
    # check_args_qnt(sys.argv)
    # Доступность файла словаря
    check_wordlist_file(args.w)
    # Доступность хоста
    if not args.e:
        set_url_format(args.u + '/')
    else:
        set_url_format(args.u + '/')

    print(f"\nРаботаем с сайтом {args.u}. Путь к словарю {args.w}\n")


def fill_dirs_from_file(dirs_file):
    """Функция читает файл с адресами папок в список"""
    with open(dirs_file, "r") as reader:
        for line in reader.readlines():
            DIRS.append(line)
    print("\nЗагружено строк из словаря: " + str(len(DIRS)) + "\n")


def write_file(text):
    with open('fuzz.txt', 'w', encoding='UTF-8') as f:
        f.write(text)


def get_site_dirs(dirs):
    """Функция проверки директорий"""
    global COUNT
    if args.e:
        dirs= dirs.strip() + '.' + args.e
    if args.uenc:
        dirs = urlparse.quote(dirs)
    if args.b64:
        dirs = str(base64.b64encode(bytes(dirs.strip(), "utf-8")), "utf-8")
    target_url = DOMAIN.replace('FUZZER', dirs.strip())
    if target_url.endswith('//'):
        target_url = target_url[:-1]
    if args.head:
        host_answer = requests.get(target_url, http_header)
        COUNT += 1
    else:
        host_answer = requests.get(target_url)
        COUNT += 1
    if 400 < host_answer.status_code < 499:
        print(
            f"{COUNT:>08d} of {len(DIRS)}\t{Fore.RED}{host_answer.status_code}{Fore.RESET}\t{target_url}                                                                                                      ",
            end='\r')
    elif 299 < host_answer.status_code < 311:
        output = f"{COUNT:>08d} of {len(DIRS)}\t{Fore.BLUE}{host_answer.status_code}{Fore.RESET}\t{target_url}"
        print(output)
    else:
        output = f"{COUNT:>08d} of {len(DIRS)}\t{Fore.GREEN}{host_answer.status_code}{Fore.RESET}\t{target_url}"
        print(output)
        write_file(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dir Fuzzer',
                                     usage='Script options')
    parser.add_argument('-u', help='Enter domain https://site.com',
                        required=True)
    parser.add_argument('-w', help='Name and path of the wordlist',
                        required=True)
    parser.add_argument('-t', type=int, help='Numbers of threads')
    parser.add_argument('-e', help='File Format')
    parser.add_argument('-b64', action='store_true',
                        help='Converts payload to base64')
    parser.add_argument('-uenc', action='store_true',
                        help='Converts payload to urlencode')
    parser.add_argument('-head', help='Send http headers with payload')
    args = parser.parse_args()
    if args.head:
        http_header = {
            (re.split(',|:', args.head))[i]: (re.split(',|:', args.head))[i + 1]
            for
            i in range(0, len((re.split(',|:', args.head))), 2)}
    greetings()
    check_app_keys()
    pool = Pool(args.t)
    pool.map(get_site_dirs, DIRS)
