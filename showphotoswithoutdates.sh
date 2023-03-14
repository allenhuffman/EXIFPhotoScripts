#!/bin/bash

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
find "$search_path" -type f -iname "*.jpg" -print0 | while IFS= read -r -d '' file; do
    # Skip filenames that start with "."
    if [[ "$(basename "$file")" =~ ^\. ]]; then
        continue
    fi

    if ! exiftool -p '$DateTimeOriginal' "$file" 2>/dev/null | grep -q '[0-9]'; then
        if [[ "$(basename "$file")" =~ _notime\..* ]]; then
            continue
        fi
        echo TODO: "$file" "${file%.*}_notime.$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')"
    fi

    # Check if file has GPS coordinates
    # if exiftool -gpslatitude -gpslongitude "$file" 2>/dev/null | grep -q '[0-9]'; then
    #     echo "$file has GPS coordinates"
    # else
    #     echo "$file does not have GPS coordinates"
    # fi

done

# End of file.
