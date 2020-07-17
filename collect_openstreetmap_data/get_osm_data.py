import overpy
api = overpy.Overpass()
import click
from geopy.geocoders import Nominatim
import pandas as pd


def build_query_from_name(name, country):
    words = name.split(' ')
    words = ['['+word[0].upper()+word[0].lower()+']'+word[1:] for word in words]
    query = '^'+'.'.join(words)
    query = query + '|' + '^[' + country[0].upper() + country[0].lower() + ']' + country[1:] + '.' + query[1:]
    return query


@click.command()
@click.option('--country', help='country name')
@click.option('--name', help='red cross name in the local language (e.g. croix rouge)')
def get_osm_data(country, name):
    """search in openstreetmap for locations of red cross branches"""

    # call OSM api (overpass)
    query_from_name = build_query_from_name(name, country)
    print('call OSM API, searching for locations named \"{}\" in {}'.format(query_from_name, country))

    query = """
    area["name"="{}"]->.boundaryarea;
    node
      ["name"~"{}"]
      (area.boundaryarea);
    out body;
    """.format(country, query_from_name)
    r = api.query(query)

    # get info on locations found
    df = pd.DataFrame()
    place_name, website, phone_number = '', '', ''
    geolocator = Nominatim(user_agent="local-branch-mapping")

    for node in r.nodes:
        place_id = node.id
        place_lat = node.lat
        place_lon = node.lon
        place_address = geolocator.reverse("{}, {}".format(place_lat, place_lon)).address
        if 'name' in node.tags.keys():
            place_name = node.tags['name']
        if 'website' in node.tags.keys():
            website = node.tags['website']
        if 'phone' in node.tags.keys():
            phone_number = node.tags['phone']
        df = df.append(pd.Series({
            'place_id': place_id,
            'place_name': place_name,
            'place_address': place_address,
            'place_lat': place_lat,
            'place_lon': place_lon,
            'phone_number': phone_number,
            'website': website,
            'country': country
        }), ignore_index=True)
        df.to_csv('search_results_'+country.lower()+'.csv')


if __name__ == '__main__':
    get_osm_data()
