"""This script for downloading jokes from the site www.anekdot.ru"""

import time
import requests
from lxml import html


def download_jokes(start_=920000, stop_=0):

    use_proxy = False
    proxy_list = ['http://122.183.139.105:8080',
                  'http://180.245.148.42:8080',
                  'http://180.248.3.82:8080']

    k = 2
    with open('jokes.txt', 'a', encoding='utf-8') as output_file:
        for n in range(start_, stop_, -1):
            url = 'http://0s.o53xo.mfxgk23en52c44tv.cmle.ru/id/{0:d}/'.format(n)
            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
            }
            proxies = {
                'http': proxy_list[k % len(proxy_list)],
                'https': proxy_list[k % len(proxy_list)]
            }
            try:
                if use_proxy:
                    r = requests.get(url, headers=headers, proxies=proxies)
                else:
                    r = requests.get(url, headers=headers)
            except TimeoutError:
                print('TimeoutError')
                k += 1
                time.sleep(10)
                continue
            except requests.exceptions.ConnectionError:
                print('requests.exceptions.ConnectionError')
                k += 1
                time.sleep(10)
                continue

            if r.status_code != requests.codes.ok:
                print(r.status_code, 'sleep for 1 seconds')
                k += 1
                time.sleep(1)
                print('try to get request')
                try:
                    if use_proxy:
                        r = requests.get(url, headers=headers, proxies=proxies)
                    else:
                        r = requests.get(url, headers=headers)
                except TimeoutError:
                    print('TimeoutError')
                    k += 1
                    time.sleep(10)
                    continue
                except requests.exceptions.ConnectionError:
                    print('requests.exceptions.ConnectionError')
                    k += 1
                    time.sleep(10)
                    continue

            current_page = html.fromstring(r.text)

            try:
                div_node = current_page.xpath('//div[@class="a_id_item"]')[0]  # find the div we need
            except IndexError:
                print('joke not found')
                continue
            text_node = div_node.xpath('./div[@class="text"]')[0]

            # add only text jokes, without links
            if len(text_node.xpath('.//img')) == 0 and len(text_node.xpath('.//a')) == 0:
                rates_node = div_node.xpath('./div[@class="rates"]')[0]
                text_of_number = 'number=' + str(n) + '\n'
                text_of_joke = '\n'.join(text_node.xpath('./text()'))
                text_of_rating = '\nrating=' + rates_node.xpath('./span[@class="value"]/text()')[0]
                print(text_of_number, end='')
                print(text_of_joke, end='')
                print(text_of_rating + '\n')
                output_file.write(text_of_number)
                output_file.write(text_of_joke)
                output_file.write(text_of_rating)
                output_file.write('\n\n')

# download_jokes()
