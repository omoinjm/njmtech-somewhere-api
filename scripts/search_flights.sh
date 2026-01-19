#!/bin/bash

# This script searches for flights using the Kiwi API (v2/search endpoint).
# Usage: ./search_flights.sh <fly_from> <fly_to> <date_from> <date_to>
# Example: ./search_flights.sh PRG LON 10/12/2024 20/12/2024

# Make sure to have jq installed to pretty-print the JSON output.
# sudo apt-get install jq (on Debian/Ubuntu)
# sudo yum install jq (on CentOS/RHEL)
# brew install jq (on macOS)

API_KEY="fUfVhV-v87mtISxkJPlasopiB3mmosJ1"
BASE_URL="https://tequila-api.kiwi.com"

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <fly_from> <fly_to> <date_from> <date_to>"
    echo "Example: $0 PRG LON 10/12/2024 20/12/2024"
    exit 1
fi

FLY_FROM="$1"
FLY_TO="$2"
DATE_FROM="$3"
DATE_TO="$4"

echo "Searching for flights from ${FLY_FROM} to ${FLY_TO} between ${DATE_FROM} and ${DATE_TO}"

curl -s -G --compressed \
  -H "apikey: ${API_KEY}" \
  -H "Content-Type: application/json" \
  --data-urlencode "fly_from=${FLY_FROM}" \
  --data-urlencode "fly_to=${FLY_TO}" \
  --data-urlencode "date_from=${DATE_FROM}" \
  --data-urlencode "date_to=${DATE_TO}" \
  "${BASE_URL}/v2/search" | jq .
