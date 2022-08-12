import pdb

from bs4 import BeautifulSoup
import requests
import re

first_page = requests.get("https://www.bbc.co.uk/schedules/p00fzl8t/2021/04/01")
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
                for elements in track.find_all('span'):
                    if elements.text == artist:
                        continue
                    title  = elements.text
                    break
                label  = track.find('abbr', { 'title': 'Record Label' })
                if label:
                    label = label.text.rstrip('. ')
                else:
                    label = 'unknown'
                # pidx   = track.text.index(title)
                # tlen   = len(title)
                # rlidx  = track.text.index(label)
                perfs  = track.contents[4].string
                if perfs:
                    rm_fill = re.compile('[\n\s]*(Performer:|Orchestra:|Conductor:|Director:|Lyricist:)[\n\s]*')
                    rm_flf  = re.compile('[\n\s]*$')
                    perfs = rm_flf.sub('', perfs)
                    perfs = rm_fill.split(perfs)[1:]
                    perfs = [p.rstrip('.') for p in perfs]
                    perfs = ' '.join(perfs)
                full   = "%s:\n%-60s %-30s\n\t%-50s %s %s" % (href, program + ':', artist + ':', title, perfs, label)
                print(full)
