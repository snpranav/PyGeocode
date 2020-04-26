#!/usr/bin/env python
"""This is a reverse geocoding script that reads a csv file and converts a latitude and longitude into an address. Furthermore, the script writes the data back into a csv of choice.
"""

__author__ = "Pranav Shikarpur"
__credits__ = "Pranav Shikarpur"
__version__ = "1.1.1"


import csv, requests, os
import pandas as pd


def user_input(state):
    disclaimer = "(Please use the letter only (A, B, C,....)"
    if state == "read_csv":
        latitude_col = input("Which column is your latitude stored in? {}\t".format(disclaimer))
        longitude_col = input("Which column is your longitude stored in? {}\t".format(disclaimer))
        
        # Formula to convert column letter into list index
        latitude_col = convert_col_letter_to_index(latitude_col)
        longitude_col = convert_col_letter_to_index(longitude_col)
        
        return latitude_col, longitude_col
    elif state == "filename":
        csv_filename = input("Please enter your input csv file name with the .csv extension:\t")
        return csv_filename
    else:
        print("Do you want to write your data to the same file or a different one?")
        output_file  = input("Hit ENTER if you want to overwrite the or enter a new filename:\t")
        return output_file

def convert_col_letter_to_index(letter):
    return ord(letter.lower()) - 96 - 1

def read_csv(csv_filename, lat_col, lng_col):
    list_of_addresses = []
    df = pd.read_csv(csv_filename)

    #Replace all NaN values with 0
    df[df.columns[lat_col]] = df[df.columns[lat_col]].fillna(0)
    df[df.columns[lng_col]] = df[df.columns[lng_col]].fillna(0)

    for index, row in df.iterrows():
        try:
            if check_if_invalid_values(row[lat_col], row[lng_col]) == False:
                response = get_geocode_API(row[lat_col], row[lng_col])
                # Appending to list of the address dictionaries
                list_of_addresses.append(parse_response(response))
            else:
                pass
        except:
            pass

    return list_of_addresses

def get_geocode_API(latitude, longitude):
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(latitude, longitude, os.environ["MAPS_API_KEY"]))
    return response.json()

def check_if_invalid_values(lat, lng):
    if lat!=0.0 or lng!=0.0:
        return False
    else:
        return True


def parse_response(response):
    try:
        address_components = response["results"][0]["address_components"]
        street_address, city, state, country, postal_code = "", "", "","",""
        for components in address_components:
            if ("premise" in components["types"]) or ("sublocality" in components["types"]):
                street_address += components["long_name"] + ", "
            if "locality" in components["types"]:
                city = components["long_name"]
            if "administrative_area_level_1" in components["types"]:
                state = components["long_name"]
            if "country" in components["types"]:
                country = components["long_name"]
            if "postal_code" in components["types"]:
                postal_code = components["long_name"]

        # Removing last comma from street address string
        street_address = street_address[:-2]

        # Creating a dictionary of address components
        address_dict = {"street_address": street_address, "city": city, "state": state, "country": country, "postal_code": postal_code}

        return address_dict
    except:
        pass

def writeto_csv(csv_filename, list_of_addresses, output_file, latitude_col, longitude_col):
    df = pd.read_csv(csv_filename)
    try:
        #Replace all NaN values with 0
        df[df.columns[latitude_col]] = df[df.columns[latitude_col]].fillna(0)
        df[df.columns[longitude_col]] = df[df.columns[latitude_col]].fillna(0)
    except:
        pass

    # To count address dictionary index
    dict_index=0
    for index, row in df.iterrows():
        try:
            if check_if_invalid_values(row[latitude_col], row[longitude_col]) == False:
                df.loc[index, 'Street'] = list_of_addresses[dict_index]["street_address"]
                df.loc[index, 'City'] = list_of_addresses[dict_index]["city"]
                df.loc[index, 'State'] = list_of_addresses[dict_index]["state"]
                df.loc[index, 'Country'] = list_of_addresses[dict_index]["country"]
                df.loc[index, 'Postal Code'] = list_of_addresses[dict_index]["postal_code"]
                dict_index += 1
            else:
                pass
        except:
            pass

    # Writing dataframe to update CSV
    if output_file == '':
        output_file=csv_filename
    
    df.to_csv(output_file, encoding='utf-8', index=False)

def main():
    csv_filename = user_input("filename")
    latitude_col, longitude_col = user_input("read_csv")
    try:
        list_of_addresses = read_csv(csv_filename, latitude_col, longitude_col)
        output_file = user_input("output_file")
        writeto_csv(csv_filename, list_of_addresses, output_file, latitude_col, longitude_col)
    except:
        output_file = user_input("output_file")
        writeto_csv(csv_filename, list_of_addresses, output_file, latitude_col, longitude_col)

if __name__ == "__main__":
    main()