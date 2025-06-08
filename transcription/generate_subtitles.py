from transformers import MarianMTModel, MarianTokenizer
import sys, os, json
import torch

# Replace <source> with the appropriate source language code, for example "de" for German.
# run without cuda:
# model_name = "Helsinki-NLP/opus-mt-de-en"
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)

model_de_en_name = "Helsinki-NLP/opus-mt-de-en"
tokenizer = MarianTokenizer.from_pretrained(model_de_en_name)
device = "cuda"
model_de_en = MarianMTModel.from_pretrained(model_de_en_name).to(device)

def translate_text(text):
    batch = tokenizer(text, return_tensors="pt", padding=True).to(device)
    translated = model_de_en.generate(**batch)
    translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return translated_text

def format_time(seconds):
    """Format seconds as SRT timestamp: HH:MM:SS,ms"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_srt(segments, language):
    """Convert transcription segments to SRT formatted string.
       Only translate if the video language is German ('de')."""
    srt_str = ""
    for i, segment in enumerate(segments, 1):
        start = format_time(segment['start'])
        end = format_time(segment['end'])
        # Only translate if the language is German; otherwise use original text.
        if language.lower() == 'de':
            text = translate_text(segment['text'].strip())
        else:
            text = segment['text'].strip()
        srt_str += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_str

def saveSRT(transcription, output_srt, language="en"):
    """Save the SRT output to file using the detected language."""
    if language not in ["en", "de"]:
        print(f"Warning: Detected language '{language}' is neither English nor German.")
    
    srt_text = create_srt(transcription.get("segments", []), language)
    with open(output_srt, "w", encoding="utf-8") as f:
        f.write(srt_text)
        
def saveTranslatedTranscription(processed_transcription, output_translated_transcription, language):
    chunks = processed_transcription.get("chunks", [])
    translated_chunks = []
    for chunk in chunks:
        if language.lower() == 'de':
            translated_text = translate_text(chunk['text'].strip())
        else:
            translated_text = chunk['text'].strip()
        translated_chunks.append({
            "text": translated_text,
            "start": chunk['start'],
            "end": chunk['end']
        })
    
    translated_transcription = processed_transcription
    translated_transcription["chunks"] = translated_chunks
    with open(output_translated_transcription, "w", encoding="utf-8") as f:
        json.dump(translated_transcription, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    transcriptions_directory = "./transcriptions"
    arguments = sys.argv
    if len(arguments) < 3:
        print("Usage: python generate_subtitles.py <start_index> <end_index>")
        sys.exit(1)
    start_index = int(arguments[1])
    end_index = int(arguments[2])
    os.makedirs("translated_transcriptions", exist_ok=True)
    os.makedirs("subtitles", exist_ok=True)
    #transcriptions_files = [f for f in os.listdir(transcriptions_directory) if f.endswith(".json")]
    #transcriptions_files.sort()
    #print(f"Found {len(transcriptions_files)} transcription files to generate subtitles for.")


    for i in range(int(start_index), int(end_index) + 1):
        filename = f"{i}_transcript.json"
        transcription_path = os.path.join(transcriptions_directory, filename)
        processed_transcription_path = os.path.join("processed_transcripts", f"{i}_transcript.json")
        
        if not os.path.exists(transcription_path) or not os.path.exists(processed_transcription_path):
            print(f"Transcription file {filename} does not exist. Skipping...")
            continue
    
      
        output_srt = os.path.join("subtitles", f"{i}_subtitles.srt")
        output_translated_transcription = os.path.join("translated_transcriptions", f"{i}_translated_transcription.json")
        
        # Skip if JSON output already exists
        if os.path.exists(output_srt) and os.path.exists(output_translated_transcription):
            print(f"Translation and translated transcript for {transcription_path} already exists. Skipping...")
            continue
        
        print(f"Generating SRT for {filename} from {start_index} to {end_index}")
        
        with open(transcription_path, "r", encoding="utf-8") as f:
            transcription = json.load(f)
        
        language = transcription.get("language", "en")
        saveSRT(transcription, output_srt, language)
        
        print(f"Saved SRT subtitles file for {filename}.")
        
        print(f"Translating transcription for {filename}...")
        with open(processed_transcription_path, "r", encoding="utf-8") as f:
            processed_transcription = json.load(f)
            
        saveTranslatedTranscription(processed_transcription, output_translated_transcription, language)
        
        
        
    
    print("All done generating subtitles and translating transcriptions!")