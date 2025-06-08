#!/bin/bash

#this script takes in 2 arguments, start and end, and will streamline the whole process of filling the database from link to transcription
#USAGE: This script must be called from a virtual environment with all necessary packages installed

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <start_id> <end_id> <cuda_device>"
    exit 1
fi

# Assign arguments to variables
start_id=$1
end_id=$2
cuda_device=$3

# Prepare virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Validate that the arguments are integers
if ! [[ "$start_id" =~ ^[0-9]+$ ]] || ! [[ "$end_id" =~ ^[0-9]+$ ]]; then
    echo "Error: Both arguments must be integers."
    exit 1
fi

# Loop through the range of video IDs and download them
echo "Downloading videos"
python3 download.py "$start_id" "$end_id"

# Call the metadata script
echo "Fetching metadata for downloaded videos..."
python3 get_metadata.py "$start_id" "$end_id"

#transcribe the videos
CUDA_VISIBLE_DEVICES=$3 python3 whisper_transcribe.py "$start_id" "$end_id"

#process transcriptions to use in database
python3 process_transcriptions.py "$start_id" "$end_id"

#translate all the videos and store srt file
CUDA_VISIBLE_DEVICES=$3 python3 generate_subtitles.py "$start_id" "$end_id"

#deactivate the virtual environment
deactivate




echo "Done!"