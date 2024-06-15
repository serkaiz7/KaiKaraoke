import os
from googleapiclient.discovery import build
import termcolor
import time
from tqdm import tqdm
import subprocess

# Replace with your own API key
API_KEY = 'YOUR_YOUTUBE_API_KEY'

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

def open_in_chrome(url):
    video_id = url.split('v=')[1]
    embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&fs=1&modestbranding=1&rel=0&showinfo=0&iv_load_policy=3"
    print(termcolor.colored(f"Opening video: {embed_url}", 'magenta'))
    # Open URL in the default browser
    subprocess.run(['termux-open', embed_url])

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
                    open_in_chrome(selected_video['link'])
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
