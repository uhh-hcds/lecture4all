import os
import chromadb
from chromadb.utils import embedding_functions
import json
from sentence_transformers import SentenceTransformer

client = chromadb.HttpClient(host="chromadb", port=8000)

model="all-mpnet-base-v2"
sentence_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model)

collection_name = "our_collection"
if collection_name in client.list_collections():
    client.delete_collection(collection_name)

collection = client.create_collection(name="our_collection", embedding_function=sentence_ef)

#path = "/processed_transcripts/"
path = "/mnt/data2/projects/w4a/l2g_download/processed_transcripts"

def add_transcript(transcript_json):
    video_id = transcript_json["id"]
    title = transcript_json["title"]
    speaker = transcript_json["speaker"]
    date = transcript_json["date"]
    category = transcript_json["category"]
    download_url = transcript_json["download"]
    thumnail_url = transcript_json["thumbnail"]
    base_metadata = {
        "video_id": video_id, 
        "title": title,
        "speaker": speaker,
        "date": date,
        "category": category,
        "download_url": download_url,
        "thumbnail_url": thumnail_url
        }

    id = 0
    for chunk in transcript_json.get("chunks", []):
        text = chunk.get("text")
        start = chunk.get("start")
        end = chunk.get("end")
        metadata = {**base_metadata, "start": start, "end": end}
        vid = f"{video_id}0{id}"
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[vid],
        )
        id += 1

j = 0
for file in os.listdir(path):
    filepath = os.path.join(path, file)
    with open(filepath, "r") as input_file:
        json_input = json.load(input_file)
    print(f"Adding transcript {json_input['id']}")
    add_transcript(json_input)
    j += 1
    if j == 4:
        break

""" video_id = json_input["id"]
metadata = [
    {"video_id": video_id}
]
i=0
for chunk in json_input.get("chunks", []):

    text = chunk.get("text")
    time = chunk.get("time")
    collection.add(
        documents=text,
        metadatas=metadata,
        ids=str(i),
    )
    i+=1 """
print("Done adding transcripts")
qtext = "this is my time, Hans"
# Query to find the nearest data
def querry_text(text,n_results):
    result = collection.query(
        query_texts=text,
        n_results=n_results
    )
    return result

def get_querry_result(text, n_results):
    formatted_result = []
    result = querry_text(text, n_results)
    length = len(result["ids"][0])
    for i in range(length):
        nr = i+1
        entry = {
            "resultNr": nr,
            "ids": result["ids"][0][i],
            "metadatas": result["metadatas"][0][i],
            "documents": result["documents"][0][i],
        }
        formatted_result.append(entry)
    return formatted_result

def format_result(result):
    result_json = {
        "videos": []
    }    
    videos = {}
    i = 1
    for entry in result:
    
        if not entry["metadatas"]["video_id"] in videos:
            video = {
                "rank" : f"{i}",
                "video_id": entry["metadatas"]["video_id"],
                "title": entry["metadatas"]["title"],
                "speaker": entry["metadatas"]["speaker"],
                "date": entry["metadatas"]["date"],
                "category": entry["metadatas"]["category"],
                "download_url": entry["metadatas"]["download_url"],
                "thumbnail_url": entry["metadatas"]["thumbnail_url"],
                "chunks": [{"text": entry["documents"],
                             "start": entry["metadatas"]["start"],
                               "end": entry["metadatas"]["end"]}]
            }
            videos[entry["metadatas"]["video_id"]] = video
            i += 1
        else:
            video = videos[entry["metadatas"]["video_id"]]
            video["chunks"].append({"text": entry["documents"],
                                    "start": entry["metadatas"]["start"],
                                    "end": entry["metadatas"]["end"]})
        result_json["videos"].append(video)
    result_json["videos"] = list(videos.values())
    return json.dumps(result_json, ensure_ascii=False, indent=4)

querry = get_querry_result(qtext, 20)
print(format_result(querry))