from googleapiclient.discovery import build

def get_youtube_video_details(video_url):
    video_id = video_url.split('v=')[-1]
    api_key = "Your API Key Here"
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch video details
    video_response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    video_details = video_response['items'][0]
    title = video_details['snippet']['title']
    thumbnail_url = video_details['snippet']['thumbnails']['high']['url']
    likes_count = video_details['statistics'].get('likeCount', 0)

    # Fetch comments
    comments = []
    comment_response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    ).execute()

    for item in comment_response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return title, thumbnail_url, likes_count, comments
