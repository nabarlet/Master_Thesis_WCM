import pdb

import sys,os
import traceback

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *['..']*2))

from bs4 import BeautifulSoup
import requests
import re
import datetime as dt
import urllib
import SPARQLWrapper

from common.utilities.string import __UNK__
import common.objects as obj
import common.wikid.wikidata as wd

class WrongDateType(ValueError):
    pass

class SingleDay:

    def __init__(self, day, provider):
        if type(day) is not dt.date:
            raise WrongDateType("%s is not a datetime.date" % str(day))
        self.day = day
        self.provider = provider

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
                            dur  = obj.Duration(__UNK__)
                            cref = track.find('span', class_='artist')
                            if cref:
                                composer = cref.text
                                for elements in track.find_all('span'):
                                    if elements.text == composer:
                                        continue
                                    title  = elements.text
                                    break
                                try:
                                    title = SingleDay.condition_title(composer, title)
                                    label = __UNK__
                                    labelhtml  = track.find('abbr', { 'title': 'Record Label' })
                                    if labelhtml:
                                        label = labelhtml.text.rstrip('. ')
                                    perfs  = SingleDay.extract_performers(track)
                                    composer = SingleDay.condition_composer(composer)
                                    (date, program_name) = self.isodate(program)
                                    perf = obj.Performance(date, self.provider, title = program_name)
                                    rec  = obj.Recording(comp=composer, oi=perfs, title=title, perf=perf, dur=dur, label=label)
                                    yield rec
                                except IndexError as e:
                                    traceback.print_exc()
                                    print("%s\n%s" % (href, e), file=sys.stderr)
                                    continue

    __BBC3_ROOT_LINK__ ="https://www.bbc.co.uk/schedules/p00fzl8t/"
    def daylink(self):
        return "%s%4d/%02d/%02d" % (SingleDay.__BBC3_ROOT_LINK__, self.day.year, self.day.month, self.day.day)

    __RM_FLF__  = re.compile('(\n+|\s{2,})')
    @staticmethod
    def condition_performers(perfs):
        result = __UNK__
        if perfs != __UNK__:
            result = SingleDay.__RM_FLF__.sub(' ', perfs)
        return result

    __EMPTY_ITEM__ = re.compile('^\s*$')
    @staticmethod
    def extract_performers(element):
        result = perfs = __UNK__
        if len(element.contents) > 6:
            perfs  = str(element.contents[4].string)
            if SingleDay.__EMPTY_ITEM__.match(perfs):
                perfs = str(element.contents[5].string)
        if perfs != __UNK__ and not SingleDay.__EMPTY_ITEM__.match(perfs):
            result = perfs
        result = SingleDay.condition_performers(result)
        return result

    @staticmethod
    def condition_title(name, title):
        result = title
        try:
            cidx = result.index(name)
            if cidx == 0:
                nl = len(name)
                result = title[nl:]
        except ValueError:
            pass
        return result

    @staticmethod
    def condition_composer(name):
        result = SingleDay.find_first_composer(name)
        try:
            result = wd.retrieve_composer(result)
        except SPARQLWrapper.SPARQLExceptions.EndPointInternalError as e:
        #except Exception as e: # urllib.error.HTTPError:
            traceback.print_exc()
            print("Error %s generated by: \"%s\"" % (e, name), file=sys.stderr)
            result = Composer(name)
        return result

    __FIRST_COMPOSER__ = re.compile(r'(\s*&\s*|\s*\/\s*|\s*[Aa][Rr][Rr]\.)')
    @staticmethod
    def find_first_composer(name):
        result = SingleDay.__FIRST_COMPOSER__.split(name)[0]
        return result

    def isodate(self, program):
        (d, m, time, title) = program.split(' ', 3)
        time = time.rstrip(':')
        (hour, min) = time.split(':')
        dtime = dt.datetime(self.day.year, self.day.month, self.day.day, int(hour), int(min), 0)
        return dtime.isoformat(), title
