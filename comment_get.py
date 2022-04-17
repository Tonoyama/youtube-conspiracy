import requests
import json
import csv

URL = 'https://www.googleapis.com/youtube/v3/'
# ここにAPI KEYを入力
API_KEY = ''

VIDEO_NAMELIST = './video_id.txt'


def video_comment(no, video_id, next_page_token):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'order': 'relevance',
    'textFormat': 'plaintext',
    'maxResults': 100,
  }
  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'commentThreads', params=params)
  resource = response.json()

  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
    # 返信数
    reply_cnt = comment_info['snippet']['totalReplyCount']
    # ユーザー名
    user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
    # Id
    parentId = comment_info['snippet']['topLevelComment']['id']

    # 出力
    parent_comment = ['{},{},{},{},{}'.format(no, text.replace('\r', '').replace('\n', ''), like_cnt, user_name, reply_cnt)]

    with open(f"./all_comment/{video_id}.csv", "a") as f:
      writer = csv.writer(f, delimiter='\n')
      writer.writerow(parent_comment)
      f.close()

    if reply_cnt > 0:
      cno = 1
      reply_comment = video_reply(no, cno, video_id, None, parentId)

      with open(f"./all_comment/{video_id}.csv", "a") as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(reply_comment)
        f.close()

    no = no + 1

  if 'nextPageToken' in resource:
    video_comment(no, video_id, resource["nextPageToken"])
  
  return parent_comment

def video_reply(no, cno, video_id, next_page_token, id):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'textFormat': 'plaintext',
    'maxResults': 50,
    'parentId': id,
  }

  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'comments', params=params)
  resource = response.json()

  reply_comment = []

  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['likeCount']
    # ユーザー名
    user_name = comment_info['snippet']['authorDisplayName']

    reply_comment += ['{}-{},{},{},{}'.format(no, cno, text.replace('\r', '').replace('\n', ''), like_cnt, user_name)]
    cno = cno + 1

  if 'nextPageToken' in resource:
    video_reply(no, cno, video_id, resource["nextPageToken"], id)
  
  return reply_comment


# コメントを全取得する

if __name__ == '__main__':
  no = 1
  with open(VIDEO_NAMELIST) as f:
    for video_id in f:
      video_id = video_id.rstrip()
      try:
        video_comment(no, video_id, None)
      except:
        print("error!!")