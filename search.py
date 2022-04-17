from apiclient.discovery import build

DEVELOPER_KEY = 'REPLACE_ME'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# https://developers.google.com/youtube/v3/docs/search/list?apix=true#try-it
search_response = youtube.search().list(
    part='snippet',  # idも指定可能。idとsnippetの両方を対象にする場合は'id,snippet'と指定する。
    q='ワクチン後遺症',
    maxResults=300, # 最大で50件
    order='viewCount',  # date, rating, relevance, title, videoCountも指定可能。
    type='video',  # channel, playlistも指定可能。複数指定する場合はカンマで区切って与える。
).execute()

print(search_response)