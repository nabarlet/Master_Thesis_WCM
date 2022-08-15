import sys,os

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *['..']*2))

import geopy
from geopy.geocoders import Nominatim
from common.utilities.string import __UNK__

__GEO__ = Nominatim(user_agent="Google_Maps")

def get_lat_long_address(place):
    location = None
    try:
        location = __GEO__.geocode(place)
    except geopy.exc.GeocoderServiceError as se:
        print("geolocation error: %s" % (se), file=sys.stderr)
    lat = long = addr = __UNK__
    if location:
        lat, long, addr = location.latitude, location.longitude, location.address
    return (lat, long, addr)
