#!/bin/bash

# Get the directory to scan from the command line, or use the current directory if none is specified
dir=${1:-.}

# Initialize a counter for the number of JPEG files found and processed
jpg_count=0

# Initialize a counter for the number of files processed
file_count=0

# Initialize a counter for the number of unique dates found
unique_date_count=0

# Create an empty dates.txt file in the directory being scanned
touch "${dir}/dates.txt"

# Recursively search for JPEG files in the specified directory and its subdirectories
find "$dir" -type f -name "*.jpg" | while read filename; do
  # Skip files that start with a dot
  if [[ $filename == .* ]]; then
    continue
  fi
  
  # Increment the file counter
  file_count=$((file_count+1))

  # Extract the EXIF date from the file using ExifTool
  exif_date=$(exiftool "$filename" | grep "Date/Time Original" | awk '{print $4}')
  
  # Skip files with -1 as the date
  if [[ $exif_date == "-1" ]]; then
    continue
  fi
  
  # Increment the JPEG file counter
  jpg_count=$((jpg_count+1))

  # Check if the date has been seen before
  if ! grep -q "$exif_date" "${dir}/dates.txt"; then
    # If the date is unique, add it to the list of dates and increment the unique date counter
    echo "$exif_date" >> "${dir}/dates.txt"
    unique_date_count=$((unique_date_count+1))
  fi
  
  # Print status every 100 files processed
  if (( file_count % 100 == 0 )); then
    echo "Processed $file_count files, found $jpg_count JPEG files, $unique_date_count unique dates"
  fi
done

# Report the number of files, JPEG files, and unique dates found
echo "Processed $file_count files, found $jpg_count JPEG files, $unique_date_count unique dates"

# Report the unique dates on which photos were taken
echo "Unique dates on which photos were taken:"
cat "${dir}/dates.txt"
