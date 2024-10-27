#!/bin/bash

mkdir -p data

DATA_URL="https://files.consumerfinance.gov/ccdb/complaints.csv.zip"

ZIP_FILE="data/complaints.csv.zip"
EXTRACTED_DIR="data"

echo "Downloading data..."
curl -o "$ZIP_FILE" "$DATA_URL"

if [ $? -eq 0 ]; then
  echo "Download successful."

  if [ -f "$ZIP_FILE" ]; then
    echo "Extracting the zip file..."
    unzip "$ZIP_FILE" -d "$EXTRACTED_DIR"

    rm "$ZIP_FILE"
    echo "Extraction completed and zip file removed."
  else
    echo "Error: Zip file not found at $ZIP_FILE"
    exit 1
  fi

else
  echo "Error: Download failed."
  exit 1
fi

echo "Data setup complete."
