# Lecture4All Transcription Scripts

## All scripts are found in the `transcription` directory

## Package Requirements

To successfully execute the scripts described, ensure the following Python packages and tools are installed in your environment:

- Python 3.x: The scripts require Python 3.x to run.
- BeautifulSoup4: A package for parsing HTML to extract metadata.
- Whisper: The Whisper model package from OpenAI, used for transcription.

To install those you can use pip:

`pip install requests beautifulsoup4 lxml whisper-timestamped transformers`

## Find Download Links

The script `find_downloadlinks.py` searches the Lecture2Go platform for videos in .mp4 format and automatically extracts their download links. These links, along with their corresponding video IDs, are saved in a .txt file, which is needed for the next step, the video download process.

How It Works

1. Configuration:
   - The script begins searching from the video ID specified by `START_ID` and continues up to `END_ID`.
   - The delay between requests, to avoid overloading the servers, is controlled by the `DELAY` parameter.
   - The output filename for the links, by default `lecture2go_links.txt`, can be set using `OUTPUT_FILE`.

2. Link Extraction:
   - Iterates over all video IDs in the specified range.
   - For each video ID, accesses the webpage and searches for an .mp4 download link.
   - Successfully found links are saved in the output file in the format `<link>;<video_id>`.

Usage

To run the script, simply use the following command in the terminal:

`python find_download.py`

At the end of the process, the file `lecture2go_links.txt` contains the video download links and can be used for the next step.

---

## Download

Once the download links have been generated, you can download the videos. The script `download.py` pulls the links from the previously created file and downloads the videos into a designated folder.

How It Works

1. Read Links:
   - Opens `lecture2go_links.txt` and reads the links line by line.

2. Download Process:
   - Checks if each video file already exists to avoid unnecessary downloads.
   - Downloads the videos with their associated video ID as the filename in .mp4 format and saves them in the "videos" folder.

Usage

To execute the script, use the following command:

`python download.py`

This starts downloading the videos into the "videos" folder. Each video is stored in the format `{video_id}.mp4`. Progress is displayed in the terminal as each video is downloaded.

---

# Transcription

Now everything is in place to start the transcription process. This is initiated using the script `whisper_transcribe.py`.

Overview

The `whisper_transcribe.py` script utilizes the Whisper model for automatic transcription of video files in the .mp4 format. It loads the model, processes each video, and saves the transcription results in JSON format.

Usage

To run the script, navigate to the directory containing the videos and execute the following command:

`python whisper_transcribe.py <start_index> <end_index>`

Parameters

- `start_index`: The index of the first video to transcribe.
- `end_index`: The index of the last video to transcribe.

## Script Details

1. Load Model: The script loads the Whisper model specified by `model_size`, which defaults to "openai/whisper-large-v2". The model is loaded using the CUDA device.

2. Transcribe Video: Each video file from the `./videos` directory is processed sequentially. The script checks if the file ends with `.mp4`, sorts the files, and then transcribes them.

3. Save Transcription: The transcribed output is saved in a directory called "transcriptions" in JSON format. If a transcription file for a specific video already exists, it will skip that video.

4. Execution Flow:
   - The script begins by loading the Whisper model.
   - It clears the console output for better visibility.
   - It loops through the video files, transcribing them from `start_index` to `end_index`.

## Output

Transcriptions are saved as JSON files in the `transcriptions` directory, with filenames in the format `<video_id>_transcript.json`. 

At the end of the process, a message "All done!" will indicate that all specified videos have been processed.

# Metadata Collection

The script `get_metadata.py` retrieves and organizes metadata for videos downloaded from Lecture2Go. It scrapes relevant information for each video from the Lecture2Go website and saves it into a JSON file for easy access and further processing.

How It Works

1. Setup Variables:
   - The base URL for accessing Lecture2Go video pages is stored in `url`.
   - The base URL for generating video thumbnail links is stored in `img`.
   - The directory where videos are stored is specified as `video_directory`.

2. Collect Video IDs:
   - The script iterates through the files in the `videos` directory, collecting video IDs from the filenames.

3. Scrape Metadata:
   - For each video ID, the script navigates to the corresponding Lecture2Go page.
   - It uses BeautifulSoup to parse the HTML and extract metadata such as title, speaker, date, and category.

4. Compile Metadata:
   - Metadata for each video, including download link, thumbnail, title, date, speaker, and category, is compiled into a dictionary and added to a list.

5. Save Metadata:
   - The metadata list is saved as a JSON file named `metadata.json`.

Usage

To execute the script, navigate to the directory containing the video files and run the following command in the terminal:

`python collect_metadata.py`

# Data Preparation for Database

The script `process_transcription_v2.py` processes transcription data and metadata, formatting it for database entry. It ensures transcription segments are appropriately organized and enriched with metadata for each video.

How It Works

1. Metadata Retrieval:
   - Before processing transcriptions, ensure metadata is updated by running `get_metadata.py`. This can also be done by this script using a subprocess call.

2. Directory Setup:
   - The script sets up a directory for  processed output files (`processed_transcripts`).

3. File Processing:
   - Iterates through each JSON file in the `transcriptions` directory, skipping already processed files.
   - For each transcription file, the corresponding metadata (such as title, speaker, and categories) is retrieved from `metadata.json`.

4. Transcription Segmentation:
   - Transcriptions are broken down into segments (or "chunks"), each approximately 12 seconds long.
   - Each chunk includes its text and time range with start and end.
   - Segments are added until they exceed the predefined time length, at which point they are saved, and processing moves to the next chunk.

5. Saving Processed Files:
   - Processed transcription data, enriched with metadata, is saved in JSON format in the `processed_transcripts` directory.

Usage

To run the script, use the following command in the terminal:

`python process_transcription_v2.py`

# Wisper4All instructions for the database and the database environment
## How to start
- go to the `/app` dirctory

- use the docker command: 
    ```bash
    docker compose up -d --build
    ```
   - if the docker image is already build you can start the container with:
   ```bash
   docker compose up -d
   ```

- now the docker containers are up and found under the following ports:
    - chroma database: *8000*
    - web-app: *5001*
    
## How to add data to the database
- use the `/app/db/add_data.py` script to add data

    1. the script can be started in the db-env container or from PC, if the the script runs on PC you need to input `localhost`  and if it is started from the container it should be `chromadb`

    2. enter the directory path with the trancripted data when asked
        - the script goes through the folder and adds all the files in the correct json format, so you have to make sure that the data has been processed correctly with the transcription scripts

## Database
- the path to the database is defined in the `.env` file as `DATABASE_PATH`

- the database is built with the latest chromadb image form the dockerhub

## Modify search results

- if you like to set the amount of chunks requested by the database, you can do so in `app/db/src/query.py` by modifing `n_results` in the `get_querry_result` function.
