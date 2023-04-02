#!/usr/bin/env python3
###############################################################################
#
# GPS Photo Sorter
# Created by ChatGPT and Allen C. Huffman
# www.subethasoftware.com
# https://github.com/allenhuffman/gps-photo-sorter
#
# Show unique focal lengths found in photos.
#
# 2023-04-01 0.00 chatgpt - Project began.
# 2023-04-01 0.10 allenh - Fixed some issues.
# 2023-04-02 0.11 allenh - Added percent of usage.
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
    description='Show unique focal lengths found in photos.',
    epilog='https://github.com/allenhuffman/gps-photo-sorter')
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

# Initialize variables to store focal lengths and total photo count
focal_lengths = {}
total_photos = 0

# Loop through all the files in the directory
for root, dirs, files in os.walk(args.path):
    for filename in files:
        if filename.endswith(".jpg"):
            # Open the file and extract the EXIF data
            with open(os.path.join(root, filename), "rb") as f:
                exif_tags = exifread.process_file(f)

            # Extract the focal length from the EXIF data
            focal_length = exif_tags.get("EXIF FocalLength")
            if focal_length is not None:
                # Add the focal length to the dictionary of focal lengths
                focal_length_str = str(focal_length)
                focal_lengths[focal_length_str] = focal_lengths.get(focal_length_str, 0) + 1
                total_photos += 1

# Print out the total number of photos scanned
print(f"{total_photos} photos scanned.")

# Print out the list of unique focal lengths with their counts and percentages
print("Unique Focal Lengths Found:", len(focal_lengths))
if args.verbose:
    for length, count in sorted(focal_lengths.items(), key=lambda x: x[1], reverse=True):
        percent = count / total_photos * 100
        print(f'{length:>12}: {count:>5} ({percent:>6.2f}%)')

# Print out the list of all focal lengths if verbose option is set
# if args.verbose:
#     print("\nAll Focal Lengths Found:")
#     for length in sorted(focal_lengths.keys()):
#         print(length)

# End of script.
