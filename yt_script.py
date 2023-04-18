import re
import requests
from bs4 import BeautifulSoup
import os
import google.auth.credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

# Set up the API client and search for videos
api_key = 'AIzaSyAdiwelV4X32OUoQHAk4s8uFGQ8i3K2iGk'
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    match = re.search(r'(?<=v=)[^&]+', url)
    return match.group(0) if match else None

new_tags = {}
def search_tag(title):
    search_query = title
    search_response = youtube.search().list(q=search_query, part='id,snippet', type='video').execute()

    # Loop through the search results and print out video details
    
    for result in search_response.get('items', []):
        video_id = result['id']['videoId']
        video_title = result['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        print(f'Title: {video_title}\nURL: {video_url}\n')
        
        # Scrape the video page to get the tags
        request = requests.get(video_url)
        html = BeautifulSoup(request.content, 'html.parser')
        tags = html.find_all('meta', property='og:video:tag')
        for tag in tags:
            # Convert tag to lowercase
            tag_lower = tag['content'].lower()
            
            # Add tag to dictionary or increment its count
            if tag_lower in new_tags:
                new_tags[tag_lower] += 1
            else:
                new_tags[tag_lower] = 1

    # Sort the dictionary by value in descending order
    new_tags_sorted = dict(sorted(new_tags.items(), key=lambda item: item[1], reverse=True))

    # Print out the dictionary of tags and their counts in descending order
    print('Tags (ordered by occurrences):')
    for tag, count in new_tags_sorted.items():
        print(f'{tag}: {count}')

    # Choose the top 15 tags and delete the others
    tags_list = list(new_tags_sorted.keys())[:15]
    tags_dict_top15 = {tag: new_tags_sorted[tag] for tag in tags_list}

    # Print out the dictionary of top 15 tags and their counts
    print('\nTop 15 tags:')
    for tag, count in tags_dict_top15.items():
        print(f'{tag}: {count}')


# Prompt user to enter a YouTube video URL
video_url = input('Enter a YouTube video URL: ')

# Extract the video ID from the URL
video_id = extract_video_id(video_url)
if not video_id:
    print('Invalid YouTube video URL')
    exit()

# Call the YouTube API to fetch video details
video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()

# Extract the tags and count their occurrences
title = video_response['items'][0]['snippet'].get('title', '')
#  Scrape the video page to get the tags
request = requests.get(video_url)
html = BeautifulSoup(request.content, 'html.parser')
tags = html.find_all('meta', property='og:video:tag')
current_tags = {}

for tag in tags:
    # Convert tag to lowercase
    tag_lower = tag['content'].lower()
        
    # Add tag to dictionary or increment its count
    if tag_lower in current_tags:
        current_tags[tag_lower] += 1
    else:
        current_tags[tag_lower] = 1

# Sort the dictionary by value in descending order
current_tags_sorted = dict(sorted(current_tags.items(), key=lambda item: item[1], reverse=True))

# Print out the dictionary of tags and their counts in descending order
print('Tags (ordered by occurrences):')
for tag, count in current_tags_sorted.items():
    print(f'{tag}: {count}')

search_tag(title)


# Call the YouTube API to update the tags of the video
update_response = youtube.videos().update(
    part='snippet',
    body={
        'id': video_id,
        'snippet': {
            'tags': new_tags
        }
    }
).execute()