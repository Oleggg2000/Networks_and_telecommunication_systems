import requests
import random
import threading
from socket import *
from bs4 import BeautifulSoup
import webbrowser

url = "file://C:/Users/Oleg/Desktop/Study/CiT/Lab_8/page.html"
proxyList = []
validproxy = []
threads = []
cashList = {}
cashPages = {}
i = 0
result = None
val = None

proxy_sock = socket(AF_INET, SOCK_STREAM)

site = "https://free-proxy-list.net/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

def parse_proxy_list():
    f = open("proxyList.txt", "w+")
    res = requests.get('https://free-proxy-list.net')
    content = BeautifulSoup(res.text, 'lxml')
    table = content.find('table')
    rows = table.find_all('tr')
    cols = [[col.text for col in row.find_all('td')] for row in rows]

    for col in cols:
        try:
            proxyList.append(col[0] + ':' + col[1])
            f.write(col[0] + ':' + col[1] + "\n")
        except:
            pass
    f.close()



def fetch_respond(url, proxy, check):
    try:
        global i, result
        #print('Trying proxy:', proxy)
        res = requests.get(url, proxies={'https': proxy}, timeout=5)
        validproxy.append(proxy)
        if check is True:
            result = res
            f = open("page.html", "wb+")
            f.write(res.content)
            f.close()
        i += 1
    except:
        return

def fetch_304_respond(url, proxy):
    try:
        global val
        res = requests.get(url, headers={"If-Modified-Since": cashList.get(url)}, proxies={'https': proxy}, timeout=5)
        val = res.status_code
    except:
        return

def foo(url, check=False):
    for proxy in proxyList:
        thread = threading.Thread(target=fetch_respond, args=(url, proxy, check,))
        thread.start()
        threads.append(thread)
    for i_thread in threads:
        if result is not None and check is True:
            break
        i_thread.join()
        threads.remove(i_thread)

def foo2(url):
    for proxy in proxyList:
        thread = threading.Thread(target=fetch_304_respond, args=(url, proxy,))
        thread.start()
        threads.append(thread)
    for i_thread in threads:
        if val is not None:
            print(val)
            break
        i_thread.join()
        threads.remove(i_thread)

def cached_site():
    foo(url, check=True)
    webbrowser.open(url, new=2)
    try:
        cashList[url] = result.headers["last-modified"]
        cashPages[url] = result.content
        # print("Last-Modified: ", result.headers["last-modified"], type(result.headers["last-modified"]), "\n")
        print(cashList, "\n")
        print(cashPages, "\n")
    except:
        print("Сайт не отдает время последней модификации Last-Modified")
        pass


parse_proxy_list()
foo("https://yandex.ru")
print("Кол-во прокси: ", len(proxyList), "Кол-во валидных прокси:", i)
print(validproxy)

while True:
    try:
        result = None
        val = None
        print("Введите url страницы:", end=" ")
        url = "https://" + input()
        with open("page.html", "w") as f:
            f.write("")
        if cashList.get(url, 0) != 0:
            foo2(url)
            if val == 200:
                cached_site()
            elif val == 304:
                print("Загрузка страницы из кэша...")
                with open("page.html", "wb+") as f:
                    f.write(b"")
                    f.write(cashPages[url])
                webbrowser.open(url, new=2)
        else:
            cached_site()
    except KeyboardInterrupt:
        break

for i_thread in threads:
    i_thread.join()
print("exiting...")


# if validproxy[0] and not validproxy[1]:
#     print(proxy[8:proxy.find(":", 8):])
#     print(proxy[proxy.find(":", 8)+1::])
#     proxy_sock.connect((proxy[8:proxy.find(":", 8):], proxy[proxy.find(":", 8)+1::]))
#     print(proxy_sock.recv(2048))