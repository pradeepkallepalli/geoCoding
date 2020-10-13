# imports
from urllib.parse import urlencode

import requests

from rsc.keys.api_keys import GOOGLE

# variables
api_key = GOOGLE.api_key


def getGeoCodeInfo(inputFormat, location):
    """

    :param inputFormat: select 'address' or 'coordinates' you are entering
    :param location: if input format is address, enter the address as string, if input format is coordinates,
                        enter the lat, long as string separated by comma e.g. '17.5127775, 78.4728904'
    :return: is a  dictionary with all address attributes
    """

    # creating the api end point with parameters
    if inputFormat.lower() == 'address':
        endPoint = f'https://maps.googleapis.com/maps/api/geocode/json'
        params = urlencode({"address": location, "key": api_key})
        url = f'{endPoint}?{params}'
    elif inputFormat.lower() == 'coordinates':
        endPoint = f'https://maps.googleapis.com/maps/api/geocode/json'
        params = urlencode({"latlng": location, "key": api_key})
        url = f'{endPoint}?{params}'
    else:
        print("Error : Please select one of the input formats['address','coordinates(latitude, longitude)']")

    # try http requests
    response = None
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"Http Error: {http_err}")
    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection Error: {conn_error}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout Error: {timeout_err}")
    except requests.exceptions.TooManyRedirects as redirect_err:
        print(f"Redirect Error: {redirect_err}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something happened {err}")

    # parsing the api response
    latitude = response.json()["results"][0]["geometry"]["location"]["lat"]
    longitude = response.json()["results"][0]["geometry"]["location"]["lng"]
    formattedAddress = response.json()["results"][0]["formatted_address"]
    houseNo = response.json()["results"][0]['address_components'][0]['long_name']
    streetAddr = response.json()["results"][0]['address_components'][1]['long_name']
    city = response.json()["results"][0]['address_components'][2]['long_name']
    county = response.json()["results"][0]['address_components'][3]['long_name']
    stateCode = response.json()["results"][0]['address_components'][4]['short_name']
    state = response.json()["results"][0]['address_components'][4]['long_name']
    countryCode = response.json()["results"][0]['address_components'][5]['short_name']
    country = response.json()["results"][0]['address_components'][5]['long_name']

    # constructing the output dictionary with all the fields needed
    geocode = {"latitude": latitude,
               "longitude": longitude,
               "formattedAddress": formattedAddress,
               "houseNo": houseNo,
               "streetAddr": streetAddr,
               "city": city,
               "county": county,
               "stateCode": stateCode,
               "state": state,
               "countryCode": countryCode,
               "country": country
               }

    return geocode


if __name__ == '__main__':
    pass
