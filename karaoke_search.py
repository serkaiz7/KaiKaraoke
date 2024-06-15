import os
import requests
from bs4 import BeautifulSoup
import termcolor
import time
from tqdm import tqdm

def search_youtube_karaoke(query):
    url = f"https://www.youtube.com/results?search_query={query}+karaoke"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for video in soup.find_all('a', {'class': 'yt-uix-tile-link'}):
        title = video.get('title')
        link = f"https://www.youtube.com{video.get('href')}"
        duration = video.find_next_sibling('span', {'class': 'video-time'}).text if video.find_next_sibling('span', {'class': 'video-time'}) else 'N/A'
        channel = video.find_next('div', {'class': 'yt-lockup-byline'}).text.strip() if video.find_next('div', {'class': 'yt-lockup-byline'}) else 'N/A'
        results.append({'title': title, 'link': link, 'duration': duration, 'channel': channel})
    
    return results

def display_results(results):
    for i, result in enumerate(results):
        print(termcolor.colored(f"{i + 1}. Title: {result['title']}", 'cyan'))
        print(termcolor.colored(f"   Channel: {result['channel']}", 'green'))
        print(termcolor.colored(f"   Duration: {result['duration']}", 'yellow'))
        print(termcolor.colored(f"   Link: {result['link']}", 'blue'))
        print('-' * 50)

def play_video(url):
    print(termcolor.colored(f"Fetching video URL...", 'magenta'))
    for _ in tqdm(range(50), desc="Processing", ascii=False, ncols=75):
        time.sleep(0.05)
    print(termcolor.colored(f"Playing video: {url}", 'magenta'))
    os.system(f"mpv $(youtube-dl -g {url})")

def main():
    print(termcolor.colored("Welcome to Karaoke Search!", 'cyan', attrs=['bold']))
    query = input("Enter the title or singer to search for karaoke videos: ")

    print(termcolor.colored("Searching for karaoke videos...", 'magenta'))
    for _ in tqdm(range(100), desc="Loading", ascii=False, ncols=75):
        time.sleep(0.03)

    results = search_youtube_karaoke(query)
    display_results(results)
    
    choice = int(input("Enter the number of the song you want to play: "))
    if 1 <= choice <= len(results):
        selected_video = results[choice - 1]
        play_video(selected_video['link'])
    else:
        print(termcolor.colored("Invalid choice. Exiting.", 'red'))

if __name__ == "__main__":
    main()
