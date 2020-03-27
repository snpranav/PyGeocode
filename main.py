#!/bin/python3

import csv, requests

def user_input():
    latitude_col = input("Which column is your latitude stored in? (Please use the letter only (A, B, C,....)\t")
    longitude_col = input("Which column is your longitude stored in? (Please use the letter only (A, B, C,....)\t")
    
    # Formula to convert column letter into list index
    latitude_col = ord(latitude_col.lower()) - 96
    longitude_col = ord(longitude_col.lower()) - 96
    
    return latitude_col, longitude_col
    

def read_csv(lat_col, lng_col):
    # Read from CSV
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count=0
        for row in csv_reader:
            get_geocode_API(row[lat_col], row[lng_col])
        #print("Lines Processed:\t" + line_count)

def get_geocode_API(latitude, longitude):
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=(lat,lng)&key=API_KEY")
    parse_response(response.json())

def parse_response(response):
    pass

def main():
    latitude_col, longitude_col = user_input()
    read_csv(latitude_col, longitude_col)

if __name__ == "__main__":
    main()