import os
from googleapiclient.discovery import build
import termcolor
import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import subprocess

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

def get_download_link(youtube_url):
    ssyoutube_url = f"https://ssyoutube.com/en212tP/youtube-to-mp4?url={youtube_url}"
    response = requests.get(ssyoutube_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the 720p download link
    download_link = None
    for link in soup.find_all('a', href=True):
        if '720' in link.text:
            download_link = link['href']
            break
    
    if download_link:
        return download_link
    else:
        print(termcolor.colored("720p link not found.", 'red'))
        return None

def open_in_mpv(url):
    print(termcolor.colored(f"Opening video in MPV player: {url}", 'magenta'))
    subprocess.run(['mpv', url])

def main():
    print(termcolor.colored("Welcome to Karaoke Search!", 'cyan', attrs=['bold']))
    
    while True:
        query = input("Enter the title or singer to search for karaoke videos: ")

        print(termcolor.colored("Searching for karaoke videos...", 'magenta'))
        for _ in tqdm(range(100), desc="Loading", ascii=False, ncols=75):
            time.sleep(0.03)

        results = search_youtube_karaoke(query)
        display_results(results)
        
        # Check if there are results before prompting for selection
        if results:
            try:
                choice = int(input("Enter the number of the song you want to play: "))
                if 1 <= choice <= len(results):
                    selected_video = results[choice - 1]
                    download_link = get_download_link(selected_video['link'])
                    if download_link:
                        open_in_mpv(download_link)
                else:
                    print(termcolor.colored("Invalid choice.", 'red'))
            except ValueError:
                print(termcolor.colored("Invalid input. Please enter a number.", 'red'))
        else:
            print(termcolor.colored("No videos to select.", 'red'))
        
        # Prompt to search again or exit
        search_again = input("Do you want to search for another song? (y/n): ").strip().lower()
        if search_again != 'y':
            print(termcolor.colored("Goodbye!", 'cyan', attrs=['bold']))
            break

if __name__ == "__main__":
    main()
