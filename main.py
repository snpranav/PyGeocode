#!/usr/bin/env python
"""This is a script that lets a user choose a task to run (geocoding or reverse geocoding)
"""

__author__ = "Pranav Shikarpur"
__credits__ = "Pranav Shikarpur"
__version__ = "1.1.0"

import os

def main():
    print("\n\nWhat is Geocoding and Reverse Geocoding?\nGeocoding - address -> location coordinates \nReverse Geocoding - location coordinates -> address\n")
    user_input = input("Do you want to geocode or REVERSE geocode your csv data? (ENTER 'g' or 'rg' respectively)\t")
    if user_input == "g":
        print("\nLet's Geocode\n")
        os.system('python3 ./geocode.py')
    elif user_input=="rg":
        print("\nLet's Reverse Geocode\n")
        os.system('python3 ./reversegeocode.py')
    else:
        print("Invalid Input. Please run the script again.")
    

if __name__ == "__main__":
    main()