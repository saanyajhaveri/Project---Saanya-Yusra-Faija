import urllib
import json
import requests
from pprint import pprint

"""URLS for requests"""
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"

"""API KEYS we retrieved from respective websites"""
MAPQUEST_API_KEY = "OyNGQIQaGmnhZ7MONyGqtgwArSMe6QA8"



def get_json(url):
    """
    This function returns Python JSON object containing the response for Mapquest
    """
    f = urllib.request.urlopen(url)
    text_response = f.read().decode('utf-8')
    response_data = json.loads(text_response)
    return response_data


def get_lat_long(place_name):
    """
    This function returns latitude and longitude after inputting place of Boston
    """
    place_name = str(place_name)
    place_name = place_name.replace(" ", "%20")
    place_name = f"{place_name},MA"
    """Ensure place is in Boston"""
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}'
    json_text = get_json(url)
    coordinates_lat_long = json_text["results"][0]["locations"][0]["latLng"]
    latitude = coordinates_lat_long["lat"]
    longitude = coordinates_lat_long["lng"]
    return longitude,latitude
def get_restaurants(place_name):
    """
        This function get coordinates info from get_lat_long() function
        and returns the name of restaurants with address within a range of 5 miles
    """
    cords=get_lat_long(place_name)
    long=cords[0]
    lat=cords[1]
    miles=8700  #in meters
    restaurants=['indian','italian','japanese','chinese','american','ethiopian','greek','mexican','thai','french'] #search any keyword
    r_result=[]
    for r in restaurants:
        url=f'https://www.mapquestapi.com/search/v4/place?' \
            f'location={long}%2C{lat}&sort=distance&feedback=true&' \
            f'key={MAPQUEST_API_KEY}&' \
            f'circle={long}%2C{lat}%2C{miles}&pageSize=50&limit=10&q={r}%2Crestaurants'
        json_text = get_json(url)
        results = json_text["results"]
        names = []
        for i in results:
            names.append(i['displayString'])
            if len(names)==15:
                break
            # names.append(i['name'])
        r=[r]
        dic=dict(enumerate(names))
        dic=dict(zip(r,[dic]))
        r_result.append(dic)
    pprint(r_result)

# place_name='Jamaica Plain Boston, MA, USA'
#place_name='Jamaica Plain, MA, USA'
#get_restaurants(place_name)


"""API KEYS we retrieved from respective websites"""
yelp_api_key='TfTXPlmj9qZohaSbmYeUt5Q5F0BOq1WRX15Zh2_45epdtnUq031z8eag8NeHYj0mxli42VCUWHntTt6m5l_10D_aykg9vrJ6DxYBIzso4i6J9AYv1ekcVd_PNueyYXYx'


def set_search_parameters(category,location,term):
    """
    This function takes search parameters from user and send it to get_details() function
    """
    params = {}
    params["categories"]=category
    params["term"] = term
    # params["ll"] = "{},{}".format(str(lat), str(long))
    params["location"]=location
    params["radius_filter"] = "8700"
    params["limit"] = "10"
    get_details(params)

def get_details(params):
    """
        This function return name ratings and address of search item
    """
    try:
        headers = {'Authorization': 'Bearer %s' % yelp_api_key}
        url = 'https://api.yelp.com/v3/businesses/search'
        req = requests.get(url, params=params, headers=headers)
        parsed = json.loads(req.text)
    
        result=[]
        businesses = parsed["businesses"]
        for business in businesses:
            a=[]
            # print("Name:", business["name"])
            a.append(business["name"])
            # print("Rating:", business["rating"])
            a.append(business["rating"])
            # print("Address:", " ".join(business["location"]["display_address"]))
            a.append( " ".join(business["location"]["display_address"]))
            result.append(a)
        keys = ["Name","Rating","Address"]
        r=[dict(zip(keys, l)) for l in result]
        pprint(r)
    except Exception:
        pass


if __name__ == '__main__':

    location=input("Enter location like 'Downtown Boston, MA, USA': ")
    term=input("Enter what you want to search like 'restaurants': ")
    category=input("Enter category like 'Chinese': ")
    set_search_parameters(category,location,term)