import re
from googleapiclient.discovery import build

# Replace YOUR_API_KEY with your actual API key
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)


video_url = input('Enter a YouTube video URL: ')
max_results = 5
tags_required = input('Enter the number of tags required (): ')


def extract_video_id(url):
    match = re.search(r'(?<=v=)[^&]+', url)
    return match.group(0) if match else None


video_id = extract_video_id(video_url)
if not video_id:
    print('Invalid YouTube video URL')
    exit()


def get_video_title(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        title = response['items'][0]['snippet']['title']
        return title
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def get_related_videos(video_title, max_results):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.search().list(
            part='snippet',
            q=video_title,
            type='video',
            maxResults=max_results
        ).execute()

        video_list = response['items']
        related_videos = []
        for video in video_list:
            title = video['snippet']['title']
            video_id = video['id']['videoId']
            related_videos.append((title, video_id))

        return related_videos
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def get_video_tags(video_id, tag_occurrences):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        tags = response['items'][0]['snippet'].get('tags', [])
        lowercase_tags = [tag.lower() for tag in tags]
        
        for tag in lowercase_tags:
            if tag in tag_occurrences:
                tag_occurrences[tag] += 1
            else:
                tag_occurrences[tag] = 1
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def update_video_tags(video_id, tags):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        video = response['items'][0]
        snippet = video['snippet']
        snippet['tags'] = tags

        update_response = youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        ).execute()

        print("Video tags updated successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

tags_ini={}
title = get_video_title(video_id)
if title:
    related_videos = get_related_videos( title, max_results)
    if related_videos:
        for video in related_videos:
            get_video_tags(video[1], tags_ini)
            
if tags_ini:
    print("\nTop Tags:")
    sorted_tags = sorted(tags_ini.items(), key=lambda x: x[1], reverse=True)
    if tags_required.isdigit() and int(tags_required) <= len(sorted_tags):
        top_tags = sorted_tags[:int(tags_required)]
    else:
        top_tags = sorted_tags
    tags_ini = dict(top_tags)
    for tag, count in tags_ini.items():
        print(f"{tag}: {count}")

tags_final={}
get_video_tags(video_id, tags_final)


tags_final.update(tags_ini)

updated_tags = list(tags_final.keys())
update_video_tags(video_id, updated_tags)
