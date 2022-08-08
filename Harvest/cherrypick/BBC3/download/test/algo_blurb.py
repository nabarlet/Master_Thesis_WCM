import pdb

from bs4 import BeautifulSoup
import requests
import re

first_page = requests.get("https://www.bbc.co.uk/schedules/p00fzl8t/2022/01/24")
first_page = first_page.text

tree = BeautifulSoup(first_page, 'html.parser')
for pbody in tree.find_all('div', attrs={ 'class': 'programme__body' }):
    for a_ref in pbody.find_all('a', attrs={ 'class': 'br-blocklink__link block-link__target', 'href': re.compile('^https:') }):
        program = a_ref.get('aria-label')
        href = a_ref.get('href')
        sub_page = requests.get(href)
        sub_page = sub_page.text
        sub_tree = BeautifulSoup(sub_page, 'html.parser')
        for spbody in sub_tree.find_all('li', attrs={ 'class': 'segments-list__item segments-list__item--music' }):
            for track in spbody.find_all('div', attrs={ 'class': 'segment__track' }):
                artist = track.find('span', class_='artist').text
                title  = track.find('p', class_='no-margin').text
                print("%-60s %-30s %s" % (program + ':', artist + ':', title))
