import os
import sys

"""
Author: w4a-backend
Description: Script to download videos from lecture2go links.
"""

import yt_dlp

def download_video(video_url):
    id = video_url.split("v/")[1]
    output_dir = "videos"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, id + ".mp4")
    
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping download.")
        return
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'./videos/{id}.%(ext)s',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            url = ""
            if info_dict.get('entries'):
                video = info_dict.get('entries')[1]
                url = video['url']
            else:
                url = video_url    

            ydl.download([url])
    except Exception as e:
        return e

#with open("lecture2go_links.txt", "r") as file:
    #links = file.read().splitlines()


def main():
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    count = 0
    err = 0
    for i in range(start, end + 1):
        link = f"https://lecture2go.uni-hamburg.de/l2go/-/get/v/{i}"
        e = download_video(link)
        if e:
            err += 1
        else:
            count += 1
        
    print(f"All done! Downloaded {count} videos. {err} Videos had an invalid ID and have not been downloaded.")


if __name__ == "__main__":
    main()

