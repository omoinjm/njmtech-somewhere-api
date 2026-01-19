#!/bin/bash

# This script searches for locations by radius using the Kiwi API (locations/radius endpoint).
# Usage: ./locations_radius.sh <latitude> <longitude> [radius_km]
# Example: ./locations_radius.sh 40.7128 -74.0060 100

# Make sure to have jq installed to pretty-print the JSON output.
# sudo apt-get install jq (on Debian/Ubuntu)
# sudo yum install jq (on CentOS/RHEL)
# brew install jq (on macOS)

API_KEY="fUfVhV-v87mtISxkJPlasopiB3mmosJ1"
BASE_URL="https://tequila-api.kiwi.com"

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <latitude> <longitude> [radius_km]"
  exit 1
fi

LAT="$1"
LON="$2"
RADIUS=${3:-250} # Default radius 250km if not provided

echo "Searching for locations within ${RADIUS}km of (${LAT}, ${LON})"

curl -s -G --compressed \
  -H "apikey: ${API_KEY}" \
  -H "Content-Type: application/json" \
  --data-urlencode "lat=${LAT}" \
  --data-urlencode "lon=${LON}" \
  --data-urlencode "radius=${RADIUS}" \
  "${BASE_URL}/locations/radius" | jq .
