#!/usr/bin/python3

"""This is a geocoding script that reads a csv file and converts a latitude and longitude into an address. Furthermore, the script writes the data back into a csv of choice.
"""

__author__ = "Pranav Shikarpur"
__credits__ = "Pranav Shikarpur"
__version__ = "1.1.0"


import csv
import requests
import os
import pandas as pd

if 'MAPS_API_KEY' not in os.environ:
    raise Exception("API Key Exception", "Script will not work. Please export your MAPS_API_KEY!")

def user_input(state):
    disclaimer = "(Please use the letter only (A, B, C,....)"
    if state == "read_csv":
        address_col = input(
            "Which column are your Addresses stored in? {}\t".format(disclaimer))
        start_index = input("Which row does the data start from (index of row starting from 0):\t")
        if int(start_index) == 0:
            raise Exception('Please insert the column name "address" in your csv to successfully run this script.')

        # Formula to convert column letter into list index
        address_col = convert_col_letter_to_index(address_col)

        return address_col, start_index
    elif state == "filename":
        csv_filename = input(
            "Please enter your input csv file name with the .csv extension:\t")
        return csv_filename
    else:
        print("Do you want to write your data to the same file or a different one?")
        output_file = input(
            "Hit ENTER if you want to overwrite the or enter a new filename:\t")
        return output_file


def convert_col_letter_to_index(letter):
    return ord(letter.lower()) - 96 - 1


def read_csv(csv_filename, address_col, start_index):
    list_of_locations = []
    list_of_addresses = []
    df = pd.read_csv(csv_filename)

    # Replace all NaN values with "blank_field"
    df[df.columns[address_col]] = df[df.columns[address_col]].fillna(
        "blank_field")

    for index, row in df.iterrows():
        if index >= int(start_index)-1:
            try:
                if check_if_invalid_values(row[address_col]) == False:
                    query_address_string = convert_address_to_query_string(
                        row[address_col])
                    response = get_geocode_API(query_address_string)
                    # Appending to list of the address dictionaries
                    if parse_response(response) != None:
                        list_of_locations.append(parse_response(response))
                        list_of_addresses.append(parse_address_response(response))
                    else:
                        list_of_locations.append({"lat": "", "lng": ""})
                else:
                    pass
            except:
                pass

    return list_of_locations, list_of_addresses


def check_if_invalid_values(address):
    if address != "blank_field":
        return False
    else:
        return True


def convert_address_to_query_string(address):
    address = address.replace(" ", "+")
    return address


def get_geocode_API(address):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?components=country:IN&address={}&key={}".format(address, os.environ["MAPS_API_KEY"]))
    return response.json()

def parse_address_response(response):
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

def parse_response(response):
    try:
        if response["status"] != "ZERO_RESULTS":
            location_dict = response["results"][0]["geometry"]["location"]
            return location_dict
        else:
            return None
    except:
        pass

def writeto_csv(csv_filename, list_of_locations, output_file, address_col, list_of_addresses, start_index):
    df = pd.read_csv(csv_filename)

    # Replace all NaN values with "blank_field"
    try:
        df[df.columns[address_col]] = df[df.columns[address_col]].fillna(
        "blank_field")
    except:
        pass

    # To count address dictionary index
    dict_index = 0
    for index, row in df.iterrows():
        if index >= int(start_index)-1:
            try:
                if check_if_invalid_values(row[address_col]) == False:
                    df.loc[index, 'Latitude'] = list_of_locations[dict_index]["lat"]
                    df.loc[index, 'Longitude'] = list_of_locations[dict_index]["lng"]                
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


    # Write address components to csv
    # To count address dictionary index
    dict_index=0
    for index, row in df.iterrows():
        if index >= int(start_index)-1:
            try:
                df.loc[index, 'Street'] = list_of_addresses[dict_index]["street_address"]
                df.loc[index, 'City'] = list_of_addresses[dict_index]["city"]
                df.loc[index, 'State'] = list_of_addresses[dict_index]["state"]
                df.loc[index, 'Country'] = list_of_addresses[dict_index]["country"]
                df.loc[index, 'Postal Code'] = list_of_addresses[dict_index]["postal_code"]
                dict_index += 1
            except:
                pass

    # Writing dataframe to update CSV
    if output_file == '':
        output_file = csv_filename

    df.to_csv(output_file, encoding='utf-8', index=False)


def main():
    csv_filename = user_input("filename")
    address_col, start_index = user_input("read_csv")
    try:
        list_of_locations, list_of_addresses = read_csv(csv_filename, address_col, start_index)
        output_file = user_input("output_file")
        writeto_csv(csv_filename, list_of_locations, output_file, address_col, list_of_addresses, start_index)
    except:
        output_file = user_input("output_file")
        writeto_csv(csv_filename, list_of_locations, output_file, address_col, list_of_addresses, start_index)


if __name__ == "__main__":
    main()
