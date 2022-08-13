import sys,os

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *['..']*2))

from geopy.geocoders import Nominatim
from common.utilities.string import __UNK__

__GEO__ = Nominatim(user_agent="Google_Maps")

def get_lat_long_address(place):
    location = __GEO__.geocode(place)
    lat = long = addr = __UNK__
    if location:
        lat, long, addr = location.latitude, location.longitude, location.address
    return (lat, long, addr)
