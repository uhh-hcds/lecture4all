import chromadb
import json
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer


client = chromadb.HttpClient(host="chromadb", port=8000)

model="all-mpnet-base-v2"
sentence_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model)

collection = client.get_collection(name="our_collection", embedding_function=sentence_ef)

qtext = "was ist ein klassiches Karteikatensystem?"
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

def process_query(query):
    querry = get_querry_result(qtext, 20)
    return format_result(querry)
