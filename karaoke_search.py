import os
import requests
from bs4 import BeautifulSoup
import termcolor
import time
from tqdm import tqdm
import webbrowser

def search_youtube_karaoke(query):
    url = f"https://www.youtube.com/results?search_query={query}+karaoke"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for video in soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-video-renderer'}):
        title = video.get('title')
        link = f"https://www.youtube.com{video.get('href')}"
        duration = video.find_next('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}).text.strip() if video.find_next('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}) else 'N/A'
        channel = video.find_next('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text.strip() if video.find_next('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}) else 'N/A'
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
    modified_url = url.replace("youtube.com", "yout-ube.com")
    print(termcolor.colored(f"Opening video in Chrome: {modified_url}", 'magenta'))
    webbrowser.open(f'googlechrome://navigate?url={modified_url}')

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
            choice = int(input("Enter the number of the song you want to play: "))
            if 1 <= choice <= len(results):
                selected_video = results[choice - 1]
                open_in_chrome(selected_video['link'])
            else:
                print(termcolor.colored("Invalid choice. Exiting.", 'red'))
        except ValueError:
            print(termcolor.colored("Invalid input. Please enter a number.", 'red'))
    else:
        print(termcolor.colored("No videos to select. Exiting.", 'red'))

if __name__ == "__main__":
    main()
