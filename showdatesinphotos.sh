#!/bin/bash
###############################################################################
#
# Sub-Etha Software's FInd Dates in Photos
# created (mostly) by chat.chatgpt.com
# with updates to make it actually work
# By Allen C. Huffman
# www.subethasoftware.com
# https://github.com/allenhuffman/EXIFPhotoScripts
#
# Recurse through JPEG photos and look for unique Date/Time codes in photos.
#
# 2023-03-13 0.01 allenh - Project began.
#
# TODO:
#
# 1) Verbose mode, so default can be silent operation.
#
# TOFIX:
#
# 1) ...
#
###############################################################################

# Function to print the help screen
print_help() {
  echo "Usage: $0 [directory]"
  echo "Recursively searches for JPEG files in [directory] (default: current directory) and reports the unique dates on which photos were taken."
  echo "Options:"
  echo "  -h, --help    Print this help message"
  exit 0
}

# Check if the user has requested the help screen
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  print_help
fi

# Get the directory to scan from the command line, or use the current directory if none is specified
dir=${1:-.}

# Initialize a counter for the number of JPEG files found
jpg_count=0

# Initialize an array to keep track of unique dates
unique_dates=()

# Recursively search for JPEG files in the current directory and its subdirectories
find "$dir" -type f -name "*.jpg" | while read filename; do
  # Skip files that start with "."
  if [[ "$(basename "$filename")" =~ ^\. ]]; then
    continue
  fi

  # Increment the JPEG file counter
  jpg_count=$((jpg_count+1))

  # Print status every 100 files processed
  if (( $jpg_count % 100 == 0 )); then
    echo "Processed $jpg_count files, unique dates found so far: ${#unique_dates[@]}"
  fi

  # Extract the EXIF date from the file using ExifTool
  exif_date=$(exiftool "$filename" | grep "Date/Time Original" | awk '{print $4}')
  
  # Skip files with -1 as the date
  if [[ $exif_date == "-1" ]]; then
    continue
  # Check if the date has been seen before
  elif [[ " ${unique_dates[@]} " =~ " ${exif_date} " ]]; then
    continue
  else
    # If the date is unique, add it to the list of dates and print it to the console
    unique_dates+=("$exif_date")
    echo "$exif_date" >> "${dir}/dates.txt"
  fi
done

# Report the number of files, JPEG files, and unique dates found
echo "Processed $jpg_count files, found $jpg_count JPEG files, ${#unique_dates[@]} unique dates"

# Report the unique dates on which photos were taken
echo "Unique dates on which photos were taken:"
cat "${dir}/dates.txt"

# End of file.
