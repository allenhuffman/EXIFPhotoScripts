#!/usr/bin/env python3
###############################################################################
#
# Sub-Etha Software's GPS Photo Sorter
# created (mostly) by chat.chatgpt.com
# with updates to make it actually work
# By Allen C. Huffman
# www.subethasoftware.com
# https://github.com/allenhuffman/xxx
#
# Show unique focal lenths found in photos.
#
# 2023-04-01 0.00 allenh - Project began.
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

# https://docs.python.org/3/library/os.html
import os
# https://pypi.org/project/ExifRead/
import exifread
# https://docs.python.org/3/library/argparse.html
import argparse

# Parse command line arguments.

parser = argparse.ArgumentParser(
                    description='Show unique focal lengths found in photos.',
                    epilog='https://github.com/allenhuffman/xxx')

parser.add_argument('--input', type=str, default='.',
                    help='Path to directory containing photos (default: photos)')

parser.add_argument('--recursive', '-r', action='store_true',
                    help='Scan photos recursively through all subdirectories')

parser.add_argument('--verbose', '-v', action='store_true',
                    help='Print out all focal lengths found')

args = parser.parse_args()

# Use args.input, args.recursive, args.verbose in your script.

print(f'Scanning photos in "{args.input}"', end='')

if args.recursive:
    print(' and all subfolders...', end='')
else:
    print('...', end='')

# Initialize an empty set to store unique focal lengths
focal_lengths = set()

# Initialize a counter variable to count the number of photos scanned
photo_count = 0

# Loop through all the files in the directory
for root, dirs, files in os.walk(args.input):
    for filename in files:
        if filename.endswith(".jpg"):
            # Increment the counter for every photo scanned
            photo_count += 1

            # Open the file and extract the EXIF data
            with open(os.path.join(root, filename), "rb") as f:
                exif_tags = exifread.process_file(f)

            # Extract the focal length from the EXIF data
            focal_length = exif_tags.get("EXIF FocalLength")
            if focal_length is not None:
                # Add the focal length to the set of unique focal lengths
                focal_lengths.add(str(focal_length))

# Print out the list of unique focal lengths and the total number of photos scanned
print(f"\nUnique Focal Lengths Found: {len(focal_lengths)} in {photo_count} photos")

if args.verbose:
    for length in sorted(focal_lengths):
        print(length)

# End of script.
