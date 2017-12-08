"""This script for downloading jokes from the site www.anekdot.ru"""

import time
import requests
from lxml import html

start = 910688
stop = 800000
with open('jokes.txt', 'a', encoding='utf-8') as output_file:
    for n in range(start, stop, -1):
        url = 'http://www.anekdot.ru/id/{0:d}/'.format(n)
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }

        r = requests.get(url, headers=headers)
        while r.status_code != 200:
            print('sleep for 5 seconds')
            time.sleep(5)
            print('try to get request')
            r = requests.get(url, headers=headers)

        current_page = html.fromstring(r.text)

        try:
            div_node = current_page.xpath('//div[@class="a_id_item"]')[0]  # find the div we need
        except IndexError:
            print('joke not found')
            continue
        text_node = div_node.xpath('./div[@class="text"]')[0]

        # add only text jokes
        if len(text_node.xpath('.//img')) == 0:
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



