import pdb

from bs4 import BeautifulSoup
import requests
import re
import datetime as dt

class WrongDateType(ValueError):
    pass

class SingleDay:

    def __init__(self, day):
        if type(day) is not dt.date:
            raise WrongDateType("%s is not a datetime.date" % str(day))
        self.day = day

    __UNKNOWN__ = 'unknown'
    def retrieve(self):
        page1 = requests.get(self.daylink()).text
        tree  = BeautifulSoup(page1, 'html.parser')
        for pbody in tree.find_all('div', attrs={  'class': 'programme__body' }):
            for a_ref in pbody.find_all('a', attrs={ 'class': 'br-blocklink__link block-link__target', 'href': re.compile('^https:') }):
                program  = a_ref.get('aria-label')
                href     = a_ref.get('href')
                subpage  = requests.get(href).text
                sub_tree = BeautifulSoup(subpage, 'html.parser')
                for spbody in sub_tree.find_all('li', attrs={ 'class': 'segments-list__item segments-list__item--music' }):
                    for track in spbody.find_all('div', attrs={ 'class': 'segment__track' }):
                        cref = track.find('span', class_='artist')
                        if cref:
                            composer = cref.text
                            for elements in track.find_all('span'):
                                if elements.text == composer:
                                    continue
                                title  = elements.text
                                break
                            label = SingleDay.__UNKNOWN__
                            labelhtml  = track.find('abbr', { 'title': 'Record Label' })
                            if labelhtml:
                                label = labelhtml.text.rstrip('. ')
                            perfs  = track.contents[4].string
                            perfs  = SingleDay.condition_performers(perfs)
                            full   = "%s:\n%-60s %-30s\n\t%-50s %s %s" % (href, program + ':', composer + ':', title, perfs, label)
                            print(full)

    __BBC3_ROOT_LINK__ ="https://www.bbc.co.uk/schedules/p00fzl8t/"
    def daylink(self):
        return "%s%4d/%02d/%02d" % (SingleDay.__BBC3_ROOT_LINK__, self.day.year, self.day.month, self.day.day)

    __RM_FILL__ = re.compile('[\n\s]*(Performer:|Orchestra:|Conductor:|Director:|Lyricist:)[\n\s]*')
    __RM_FLF__  = re.compile('[\n\s]*$')
    @staticmethod
    def condition_performers(perfs):
        result = SingleDay.__UNKNOWN__
        if perfs:
            result = SingleDay.__RM_FLF__.sub('', perfs)
            result = SingleDay.__RM_FILL__.split(result)[1:]
            result = [p.rstrip('.') for p in result]
            result = ' '.join(result)
        return result
