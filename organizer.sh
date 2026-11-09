#!/bin/bash

# Create the archive directory if it does not exist
mkdir -p archive

if [ ! -f grades.csv ]; then
    echo "Error: grades.csv not found in the current directory."
    exit 1
fi

timestamp=$(date +%Y%m%d-%H%M%S)
archived="grades_${timestamp}.csv"

# Archive the current file, then reset the workspace
mv grades.csv "archive/$archived"
touch grades.csv

# Append to the log
echo "[$timestamp] Original: grades.csv | Archived: archive/$archived" >> organizer.log

echo "Archived grades.csv to archive/$archived"
