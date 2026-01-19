#!/bin/bash

# This script searches for locations using the Kiwi API (locations/query endpoint).
# Usage: ./locations_query.sh <search_term>
# Example: ./locations_query.sh "New York"

# Make sure to have jq installed to pretty-print the JSON output.
# sudo apt-get install jq (on Debian/Ubuntu)
# sudo yum install jq (on CentOS/RHEL)
# brew install jq (on macOS)

API_KEY="fUfVhV-v87mtISxkJPlasopiB3mmosJ1"
BASE_URL="https://tequila-api.kiwi.com"

if [ -z "$1" ]; then
  echo "Usage: $0 <search_term>"
  exit 1
fi

SEARCH_TERM="$1"

echo "Searching for location: ${SEARCH_TERM}"

curl -s -G --compressed \
  -H "apikey: ${API_KEY}" \
  -H "Content-Type: application/json" \
  --data-urlencode "term=${SEARCH_TERM}" \
  "${BASE_URL}/locations/query" | jq .
