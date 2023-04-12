#!/usr/bin/env python3
###############################################################################
#
# Show Unique GPS Coordinates
# Created by ChatGPT and Allen C. Huffman
# www.subethasoftware.com
# https://github.com/allenhuffman/EXIFPhotoScripts
#
# Show unique GPS coordinates found in photos.
#
# 2023-04-11 0.00 chatgpt - Project began.
#
# TODO:
#
# 1) ...
#
# TOFIX:
#
# 1) ...
#
###############################################################################

import os
import exifread
import argparse

# Parse command line arguments.
parser = argparse.ArgumentParser(
    description='Show unique GPS coordinates found in photos.',
    epilog='https://github.com/allenhuffman/EXIFPhotoScripts')
parser.add_argument('path', nargs='?', default='.',
                    help='path to directory containing photos (default: current directory)')
parser.add_argument('--recursive', '-r', action='store_true',
                    help='scan photos recursively through all subdirectories')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print out all focal lengths found')
args = parser.parse_args()

print(f"Scanning photos in '{args.path}'", end='')
if args.recursive:
    print(' and all subfolders...')
else:
    print('...')

def get_gps_from_image(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            lat_ref = tags['GPS GPSLatitudeRef'].values
            lat = tags['GPS GPSLatitude'].values
            lon_ref = tags['GPS GPSLongitudeRef'].values
            lon = tags['GPS GPSLongitude'].values

            lat_degrees = float(lat[0].num) / float(lat[0].den)
            lat_minutes = float(lat[1].num) / float(lat[1].den)
            lat_seconds = float(lat[2].num) / float(lat[2].den)
            lat = lat_degrees + (lat_minutes / 60.0) + (lat_seconds / 3600.0)
            if lat_ref == 'S':
                lat = -lat

            lon_degrees = float(lon[0].num) / float(lon[0].den)
            lon_minutes = float(lon[1].num) / float(lon[1].den)
            lon_seconds = float(lon[2].num) / float(lon[2].den)
            lon = lon_degrees + (lon_minutes / 60.0) + (lon_seconds / 3600.0)
            if lon_ref == 'W':
                lon = -lon

            return (lat, lon)
        else:
            return None


# Function to recursively find all JPG files in a directory and its subdirectories
def find_jpg_files(dir_path):
    jpg_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                if args.verbose:
                    print(file)
                jpg_files.append(os.path.join(root, file))

    return jpg_files

# Main function to count unique GPS coordinates in all JPG files in a directory
def count_unique_gps_coordinates(dir_path):
    gps_coordinates = set()
    jpg_files = find_jpg_files(dir_path)
    num_images = len(jpg_files)
    for i, file_path in enumerate(jpg_files):
        gps = get_gps_from_image(file_path)
        if gps is not None:
            if args.verbose:
                print(gps)
            gps_coordinates.add(gps)
        print(f"Processed {i+1} out of {num_images} images...", end="\r")
    print() # Print newline to clear line of previous output
    return len(gps_coordinates)

# Example usage:
dir_path = args.path
num_unique_gps_coordinates = count_unique_gps_coordinates(dir_path)
print("Number of unique GPS coordinates in your photos:", num_unique_gps_coordinates)

# End of showuniquelocations.py
