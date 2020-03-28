#!/usr/bin/python3

"""This is a geocoding script that reads a csv file and converts a latitude and longitude into an address. Furthermore, the script writes the data back into a csv of choice.
"""

__author__ = "Pranav Shikarpur"
__credits__ = "Pranav Shikarpur"
__version__ = "1.1.0"


import csv, requests, os
import pandas as pd

def user_input(state):
    disclaimer = "(Please use the letter only (A, B, C,....)"
    if state == "read_csv":
        address_col = input("Which column are your Addresses stored in? {}\t".format(disclaimer))
        
        # Formula to convert column letter into list index
        address_col = convert_col_letter_to_index(address_col)
        
        return address_col
    elif state == "filename":
        csv_filename = input("Please enter your input csv file name with the .csv extension:\t")
        return csv_filename
    else:
        print("Do you want to write your data to the same file or a different one?")
        output_file  = input("Hit ENTER if you want to overwrite the or enter a new filename:\t")
        return output_file

def convert_col_letter_to_index(letter):
    return ord(letter.lower()) - 96 - 1

def read_csv(csv_filename, address_col):
    list_of_locations = []
    df = pd.read_csv(csv_filename)

    #Replace all NaN values with "blank_field"
    df[df.columns[address_col]] = df[df.columns[address_col]].fillna("blank_field")

    for index, row in df.iterrows():
        if check_if_invalid_values(row[address_col]) == False:
            query_address_string = convert_address_to_query_string(row[address_col])
            response = get_geocode_API(query_address_string)
            # Appending to list of the address dictionaries
            list_of_locations.append(parse_response(response))
        else:
            pass

    return list_of_locations

def check_if_invalid_values(address):
    if address!="blank_field":
        return False
    else:
        return True

def convert_address_to_query_string(address):
    address = address.replace(" ", "+")
    return address

def get_geocode_API(address):
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, os.environ["MAPS_API_KEY"]))
    return response.json()

def parse_response(response):
    location_dict = response["results"][0]["geometry"]["location"]
    return location_dict

def writeto_csv(csv_filename, list_of_locations, output_file, address_col):
    df = pd.read_csv(csv_filename)

    #Replace all NaN values with "blank_field"
    df[df.columns[address_col]] = df[df.columns[address_col]].fillna("blank_field")

    for index, row in df.iterrows():
        if check_if_invalid_values(row[address_col]) == False:
            df.loc[index, 'Latitude'] = list_of_locations[index]["lat"]
            df.loc[index, 'Longitude'] = list_of_locations[index]["lng"]
        else:
            pass

    # Writing dataframe to update CSV
    if output_file == '':
        output_file=csv_filename
    
    df.to_csv(output_file, encoding='utf-8', index=False)

def main():
    csv_filename = user_input("filename")
    address_col = user_input("read_csv")
    list_of_locations = read_csv(csv_filename, address_col)
    output_file = user_input("output_file")
    writeto_csv(csv_filename, list_of_locations, output_file, address_col)

if __name__ == "__main__":
    main()