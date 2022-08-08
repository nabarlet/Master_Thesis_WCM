# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys,os
import http
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from SPARQLWrapper import SPARQLWrapper, JSON
from common.objects.composer import Composer
from common.objects.timeline import TimeLine, ComposerAgeIsZero
import pdb


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def sparql_composer(nid):
    final_result=None
    endpoint_url = "https://query.wikidata.org/sparql"
    query = "SELECT distinct ?person ?personLabel ?personDescription ?birth ?death ?countryLabel ?genderLabel ?coords ?lat ?long ?movementLabel ?precisiondob ?precisiondod WHERE {\
             VALUES (?person) {(wd:%s)}\
             ?person wdt:P31 wd:Q5;\
             p:P569/psv:P569  [wikibase:timeValue ?birth; wikibase:timePrecision ?precisiondob].\
             OPTIONAL {?person p:P570/psv:P570 [wikibase:timeValue ?death; wikibase:timePrecision ?precisiondod].}\
             OPTIONAL {?person wdt:P27 ?country .}\
             OPTIONAL {?person wdt:P21 ?gender .}\
             OPTIONAL {?country p:P625 ?coords_sample .}\
             OPTIONAL {?coords_sample ps:P625 ?coords; psv:P625 [ wikibase:geoLatitude ?lat; wikibase:geoLongitude ?long ] .}\
      OPTIONAL {?person wdt:P135 ?movement .}\
      SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\" }\
} ORDER BY DESC (?precisiondob) DESC(?precisiondod) (?country)\n" % (nid)

    tl = TimeLine.create_from_csv()
    try:
        results=get_results(endpoint_url, query)
        results=results['results']['bindings']
        if len(results)>0:  
            death = None
            country = gender = lat = long = 'unknown'
            movement=None
            result=results[0]   
            name = result['personLabel']['value']
            birth = result['birth']['value']
            if 'death' in result:
                death = result['death']['value']
            if 'countryLabel' in result:
                country = result['countryLabel']['value']
            if 'genderLabel' in result:
                gender = result['genderLabel']['value']
            if 'lat' in result:
                lat = result['lat']['value']
            if 'long' in result:
                long = result['long']['value']
            final_result= Composer(name,birth,death, nid=nid, country=country, gender=gender, lat=lat, long=long)
            try:
                movement = tl.assign_movement(final_result)
                final_result.movement = movement
            except ComposerAgeIsZero:
                print("Composer " + final_result.name + " age is zero! No movement defined", file=sys.stderr)
    except http.client.IncompleteRead as e:
            print(str(e) + ' Continuing.', file=sys.stderr)
        
    return final_result
    
def sparql_periods():
    result=None
    endpoint_url = "https://query.wikidata.org/sparql"
    #query=
    result=get_results(endpoint_url, query)
''' 
    Medieval= (500 – 1400)
        • Ars antiqua c. 1170 – c. 1310
        • Ars nova    c. 1310 – c. 1377
        • Ars subtilior   c. 1360 – c. 1420
    Renaissance c. 1400 – c. 1600
        • Transition to Baroque   

    Baroque =(1580 – 1750)
    • Galant music    c. 1720 – c. 1770
    • Empfindsamkeit  c. 1740 – c. 1780
    Classical = (1750 – 1820)
        • Mannheim school c. 1740 – c. 1780
        • Sturm und Drang c. 1770
        • Transition to Romantic  
    Romantic = (1800 – 1910)
    Late 19th-, 20th- and 21st-centuries
    Modernism = (1890 – 1975)
        • Impressionism   c. 1890 – c. 1930
        • Expressionism   c. 1900 – c. 1930
        • Neoclassicism   c. 1920 – c. 1950
        • Serialism   c. 1920 – c. 1975
    Contemporary    from c. 1950
        • Minimalism  from c. 1960
        • Postmodernism   from c. 1960s
        • Postminimalism  from c. 1980
'''   
            # date of birth (P569) 
            # date of death (P570) 
            # place of birth (P19) 
            # place of death (P20) 
            
#select distinct ?person ?personLabel ?personDescription ?birth ?death ?movementLabel where {
 # VALUES (?person) {(wd:Q1339)}
 #   ?person wdt:P31 wd:Q5; 
  #        wdt:P106 wd:Q36834;
  #          p:P570/psv:P570 [wikibase:timeValue  ?death ]; 
#           p:P569/psv:P569  [wikibase:timeValue ?birth];
 #           wdt:P135 ?movement
            
   
 #   SERVICE wikibase:label { bd:serviceParam wikibase:language "en,en" }
#}

