import os
import requests
from googleapiclient.discovery import build
import termcolor
import time
from tqdm import tqdm
import subprocess
import yt_dlp

# Replace with your own API key
API_KEY = 'AIzaSyDJh3-sX1WNW4Cz5LA3jEtPSUGmqwall3k'

def search_youtube_karaoke(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part='snippet',
        q=f"{query} karaoke",
        type='video',
        maxResults=10
    )
    response = request.execute()
    
    results = []
    for item in response['items']:
        title = item['snippet']['title']
        link = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        channel = item['snippet']['channelTitle']
        duration = 'N/A'  # You can fetch video details in another API call if needed
        results.append({'title': title, 'link': link, 'duration': duration, 'channel': channel})
    
    return results

def display_results(results):
    if not results:
        print(termcolor.colored("No results found. Please try a different query.", 'red'))
        return
    for i, result in enumerate(results):
        print(termcolor.colored(f"{i + 1}. Title: {result['title']}", 'cyan'))
        print(termcolor.colored(f"   Channel: {result['channel']}", 'green'))
        print(termcolor.colored(f"   Duration: {result['duration']}", 'yellow'))
        print(termcolor.colored(f"   Link: {result['link']}", 'blue'))
        print('-' * 50)

def fetch_video_url(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_url = info_dict.get("url", None)
    return video_url

def open_in_mpv(url):
    mod_url = url.replace("youtube.com", "yout-ube.com")
    print(termcolor.colored(f"Fetching direct video URL for: {mod_url}", 'magenta'))
    
    video_url = fetch_video_url(url)
    if video_url:
        print(termcolor.colored(f"Playing video in MPV: {video_url}", 'magenta'))
        try:
            subprocess.run(['mpv', '--fullscreen', video_url], check=True)
        except FileNotFoundError:
            print(termcolor.colored("MPV not found. Please ensure MPV is installed and in your PATH.", 'red'))
        except subprocess.CalledProcessError as e:
            print(termcolor.colored(f"An error occurred while trying to play the video: {e}", 'red'))
    else:
        print(termcolor.colored("Failed to fetch video URL.", 'red'))

def main():
    print(termcolor.colored("Welcome to Karaoke Search!", 'cyan', attrs=['bold']))
    query = input("Enter the title or singer to search for karaoke videos: ")

    print(termcolor.colored("Searching for karaoke videos...", 'magenta'))
    for _ in tqdm(range(100), desc="Loading", ascii=False, ncols=75):
        time.sleep(0.03)

    results = search_youtube_karaoke(query)
    display_results(results)
    
    # Check if there are results before prompting for selection
    if results:
        try:
            choice = int(input("Enter the number of the song you want to play: "))if 1 <= choice <= len(results):
                selected_video = results[choice - 1]
                open_in_mpv(selected_video['link'])
            else:
                print(termcolor.colored("Invalid choice. Exiting.", 'red'))
        except ValueError:
            print(termcolor.colored("Invalid input. Please enter a number.", 'red'))
    else:
        print(termcolor.colored("No videos to select. Exiting.", 'red'))

if __name__ == "__main__":
    main()
