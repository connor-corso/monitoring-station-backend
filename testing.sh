#!/bin/bash

# Function to generate a random number between 1 and 100 (adjust range as needed)
function generate_random_number() {
  echo $((RANDOM % 100 + 1))
}

# Main loop
for ((i=1; i<=30; i++)); do
  # Get the current epoch time in seconds
  current_epoch=$(date +%s)

  # Generate a random number
  random_number=$(generate_random_number)

  # Output the results for this run
  echo "Run $i:"
  echo "Current Epoch: $current_epoch"
  echo "Random Number: $random_number"

  # POST data to the API using curl
  curl -X 'POST' 'https://monitoring-station-backend.ccorso.ca/create-record/5/' \
    -H 'Content-Type: application/json' \
    -d '{
      "datetime": '"$current_epoch"',
      "data": '"$random_number"',
      "owner_id": 1
    }'

  # Wait for 60 seconds before the next run
  sleep 60
done
