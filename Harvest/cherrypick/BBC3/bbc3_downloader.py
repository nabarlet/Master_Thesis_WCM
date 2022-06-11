import pdb
import os,sys
sys.path.append('..')
import yaml
import tweepy
import json
import re
import datetime as dt
from common.objects.recording import Recording

root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root_path)
from cherrypick.base import Base
from bbc3_base import BBC3Base

class BBC3Downloader(Base):

    __DEFAULT_BBC3_ID__ = 'BBCR3MusicBot'
    
    def __init__(self):
        super().__init__()
        self.auth=self.load_credentials()
        self.api=tweepy.API(self.auth,parser=tweepy.parsers.JSONParser())
        #
        # as a default, we set the download limit to a very high number which
        # will never be reached
        #
        self.limit=6000000
        
            
    def download(self):
        for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=BBC3Downloader.__DEFAULT_BBC3_ID__).items(self.limit):
            yield tweet
            
    def inspect(self):
        for item in self.download():
            yield json.dumps(item,sort_keys=True,indent=4)
            
    # TO-DO:
    # use the api of wikidata to complete title data

    
    def parse(self):
        for item in self.download():
            found = not_found = None
            text = item["text"]
            date = item["created_at"]
            hre = re.compile("\ANow Playing ") #head regexp
            tre = re.compile("[@#].*\Z") #tail regexp
            data = hre.sub('',text) #replace Now Playing with nothing
            data = tre.sub('',data) #replace # whatever with nothing
            (humans,title) = data.split(' - ',1)
            humans = humans.split(', ') #array
            composer = self.retrieve_composer(humans[0])
            pdate = BBC3Base.process_date(date)
            composer.perf_date = pdate.isoformat()
            performers=None
            if len(humans)>1:
                performers=humans[1:]
            complete_title = self.expand_title(title)   
            gotcha = Recording(composer,performers,complete_title,date)
            if composer.birth:
                found = gotcha
            else:
                not_found = gotcha
            yield found, not_found
    
    def expand_title(self,title):
        result=title
        return result
        
    # PLEASE NOTE
    # The credentials file is not present in the repository for obv reasons 
    # you have to provide it and call it Twitter_auth.yaml and it has to be placed in
    # the same directory as this file
            
    __CREDENTIALS_FILE__= 'Twitter_auth.yaml' 
    def load_credentials(self):
        y=yaml.safe_load(open(BBC3Downloader.__CREDENTIALS_FILE__,'r'))
        if not y:
            raise FileNotFoundError
        auth = tweepy.OAuthHandler(y['consumer_key'],y['consumer_secret'])
        auth.set_access_token(y['access_token_key'], y['access_token_secret'])
        return auth
