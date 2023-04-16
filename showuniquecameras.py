#!/usr/bin/env python3
###############################################################################
#
# Show Unique Cameras
# Created by ChatGPT
#
# Show unique cameras found in photos.
#
# 2023-04-15 0.00 chatgpt - Project began.
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
    description='Show unique cameras found in photos.',
    epilog='https://github.com/allenhuffman/EXIFPhotoScripts')
parser.add_argument('path', nargs='?', default='.',
                    help='path to directory containing photos (default: current directory)')
parser.add_argument('--recursive', '-r', action='store_true',
                    help='scan photos recursively through all subdirectories')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print out all cameras found')
args = parser.parse_args()

print(f"Scanning photos in '{args.path}'", end='')
if args.recursive:
    print(' and all subfolders...')
else:
    print('...')

def get_camera_from_image(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        if 'Image Make' in tags and 'Image Model' in tags:
            camera_make = str(tags['Image Make'].values).strip()
            camera_model = str(tags['Image Model'].values).strip()
            camera = camera_make + " " + camera_model
            return camera
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

# Main function to get list of unique cameras used in all JPG files in a directory
def get_unique_cameras(dir_path):
    cameras = set()
    jpg_files = find_jpg_files(dir_path)
    num_images = len(jpg_files)
    for i, file_path in enumerate(jpg_files):
        camera = get_camera_from_image(file_path)
        if camera is not None:
            if args.verbose:
                print(camera)
            cameras.add(camera)
        print(f"Processed {i+1} out of {num_images} images...", end="\r")
    print() # Print newline to clear line of previous output
    return cameras

# Example usage:
dir_path = args.path
unique_cameras = get_unique_cameras(dir_path)
print("List of unique cameras used in your photos:")
for camera in unique_cameras:
    print(camera)

# End of showuniquecameras.py
