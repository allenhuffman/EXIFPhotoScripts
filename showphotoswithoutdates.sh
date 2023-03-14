#!/bin/bash
###############################################################################
#
# Sub-Etha Software's Show Photos Without Dates
# created (mostly) by chat.chatgpt.com
# with updates to make it actually work
# By Allen C. Huffman
# www.subethasoftware.com
# https://github.com/allenhuffman/ShowDatesInPhotos
#
# Recurse through JPEG photos and report ones that are missing Date/Time.
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
  echo "Recursively searches for JPEG files in [directory] (default: current directory) and report any that do not have Date/Time."
  echo "Options:"
  echo "  -h, --help    Print this help message"
  exit 0
}

# Check if the user has requested the help screen
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  print_help
fi

search_path="${1:-.}"

jpg_count=0
nodate_count=0

find "$search_path" -type f -iname "*.jpg" -print0 | while IFS= read -r -d '' file; do
    # Skip filenames that start with "."
    if [[ "$(basename "$file")" =~ ^\. ]]; then
        continue
    fi

    jpg_count=$((jpg_count+1))

    # echo $file

    if ! exiftool -p '$DateTimeOriginal' "$file" 2>/dev/null | grep -q '[0-9]'; then
        if [[ "$(basename "$file")" =~ _notime\..* ]]; then
            continue
        fi

        nodate_count=$((nodate_count+1))

        echo TODO: mv "$file" "${file%.*}_notime.$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')"
    fi

    # if (( $jpg_count % 100 == 0 )); then
    #     echo "Processed $jpg_count files, no dates found in $nodate_count so far."
    # fi

    # Check if file has GPS coordinates
    # if exiftool -gpslatitude -gpslongitude "$file" 2>/dev/null | grep -q '[0-9]'; then
    #     echo "$file has GPS coordinates"
    # else
    #     echo "$file does not have GPS coordinates"
    # fi

done

# End of file.
