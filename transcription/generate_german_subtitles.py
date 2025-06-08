import os
import sys
import json

def format_time(seconds):
    """Format seconds as SRT timestamp: HH:MM:SS,ms"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_srt(segments):
    """Convert transcription segments to SRT formatted string."""
    srt_str = ""
    for i, segment in enumerate(segments, 1):
        start = format_time(segment['start'])
        end = format_time(segment['end'])
        text = segment['text'].strip()
        srt_str += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_str

def save_srt(transcription, output_srt):
    """Save the SRT output to file using the transcription segments."""
    srt_text = create_srt(transcription.get("segments", []))
    with open(output_srt, "w", encoding="utf-8") as f:
        f.write(srt_text)

if __name__ == "__main__":
    # Usage: python generate_german_subtitles.py <start_index> <end_index>
    if len(sys.argv) < 3:
        print("Usage: python generate_german_subtitles.py <start_index> <end_index>")
        sys.exit(1)

    start_index = int(sys.argv[1])
    end_index = int(sys.argv[2])

    transcriptions_directory = "./transcriptions"
    os.makedirs("subtitles", exist_ok=True)

    for i in range(start_index, end_index + 1):
        filename = f"{i}_transcript.json"
        transcription_path = os.path.join(transcriptions_directory, filename)
        
        if not os.path.exists(transcription_path):
            print(f"Transcription file {filename} does not exist. Skipping...")
            continue
        
        with open(transcription_path, "r", encoding="utf-8") as f:
            transcription = json.load(f)
        
        detected_language = transcription.get("language", "en").lower()
        if detected_language != "de":
            print(f"Skipping {filename}: Detected language '{detected_language}' is not German.")
            continue

        output_srt = os.path.join("subtitles", f"{i}_subtitles_de.srt")
        print(f"Generating German SRT for {filename}...")
        save_srt(transcription, output_srt)
        print(f"Saved German SRT subtitles file for {filename} as {output_srt}.")

    print("All done generating German subtitles!")