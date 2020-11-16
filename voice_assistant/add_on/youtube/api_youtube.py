import requests
from pprint import pprint
import urllib.parse
import time
import json

import random


class Youtube:
    def __init__(self):
        self.API_KEY = ['AIzaSyDqaXiQY9qKj63yws71b7opNAixmRVcPTo','AIzaSyCgYhNkV3x0sj0aheyojiXwa2mhmOCtc44']

    def dictResult(self, arr):
        """
        辞書形にして変換するメソッド
        :param arr: list
        :return:
        """
        self.result = {
            'result': arr
        }
        pprint(self.result)

    def videoInfo(self, video_id):
        """
        動画情報を表示するメソッド
        :param video_id: str 7BzGOVk0J-s ← v=parameter  youtubeURL https://www.youtube.com/watch?v=7BzGOVk0J-s&t=1s,
        :return: dict {
                    'result':[
                        {
                            'title' : 動画タイトル,
                            'publishedAt' : 動画投稿日時,
                            'channelTitle': 投稿ユーザー名,
                            'tags': 動画についているタグ,
                            'description': 動画の説明欄,
                            'viewCount': 視聴回数,
                            'likeCount': good数,
                            'dislikeCount': bad数,
                            'commentCount': コメント数
                        },
                    ]
                }
        """
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        URL = 'https://www.googleapis.com/youtube/v3/videos'
        parts = ['snippet','contentDetails','statistics','status']
        ids = [video_id]
        part = ','.join([part for part in parts]) 
        payload = {
            'part': part,
            'id': ','.join(ids),
            'key': API_KEY,
        }
        r = requests.get(URL, params=payload)
        res = r.json()
        snippet = res['items'][0]['snippet']
        statistics= res['items'][0]['statistics']
        video_info = {
            'title': snippet['title'],
            'publishedAt': snippet['publishedAt'],
            'channelTitle': snippet['channelTitle'],
            'tags': snippet['tags'],
            'description': snippet['description'],
            'viewCount': statistics['viewCount'],
            'likeCount': statistics['likeCount'],
            'dislikeCount': statistics['dislikeCount'],
            'commentCount': statistics['commentCount']
        }
        self.dictResult([video_info])

    def channelIdSearch(self, channel_name):
        """
        channelTitleからchannelIdを検索するメソッド
        :param channel_name: str チャンネルの名前
        :return: dict {
                    'result':[
                        {
                            'title' : channelTitle ,
                            'id' : channelId
                        },
                        ]
                    }
        """
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        result = []
        URL = 'https://www.googleapis.com/youtube/v3/search'
        payload = {
            'part': 'snippet',
            'q': channel_name,
            'key': API_KEY,
        }
        r = requests.get(URL, params=payload)
        res = r.json()
        items = res['items']
        for item in items:
            keys = list(item['id'].keys())
            if keys[1] == 'channelId':
                channel_info = {
                    'title': item['snippet']['channelTitle'],
                    'id': item['id']['channelId'],
                }

                result.append(channel_info)
        self.dictResult(result)

    def get_correct_requests(self, URL, parts, channel_id, API_KEY):
        ids = [channel_id]
        part = ','.join([part for part in parts])
        payload = {
            'part': part,
            'id': ','.join(ids),
            'key': API_KEY,
        }
        r = requests.get(URL, params=payload)

        if str(r) == '<Response [200]>':
            self.res = r.json()
        else:
            to_remove = json.loads(r.text)['error']['message'].replace("'", '')
            parts.remove(to_remove)
            self.get_correct_requests(URL, parts, channel_id, API_KEY)

    def check_json_key(self, key, json):
        if key in json:
            return key

    def channelInfo(self, channel_id):
        """
        チャンネルの情報を取得するメソッド
        :param channel_id: str
        :return:  dict {
                    result:[
                        {
                            'title' : チャンネルユーザー名,
                            'description' : チャンネルの説明,
                            'publishedAt': チャンネルの開設日,
                            'keywards': チャンネルの検索キーワード,
                            'viewCount' : 投稿した動画のそう視聴回数,
                            'commentCount': 動画にコメントした回数,
                            'subscriberCount': goodの総数,
                            'videoCount': 投稿した動画の本数,
                            'uploads': 投稿した動画リストのID
                        },
                    ]
                }
        """
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        URL = 'https://www.googleapis.com/youtube/v3/channels'
        parts = ['snippet', 'brandingSettings', 'contentDetails', 'invideoPromotion', 'invideoPromotions', 'statistics', 'status', 'topicDetails']

        self.get_correct_requests(URL, parts, channel_id, API_KEY)

        first_level_json = ['brandingSettings', 'snippet', 'contentDetails', 'statistics']
        second_level_json = {'snippet': ['title', 'description', 'publishedAt'],
                             'brandingSettings': ['keywords'],
                             'statistics': ['viewCount', 'commentCount', 'subscriberCount', 'videoCount'],
                             'contentDetails': ['uploads']}
        channel_info = {}
        for key in first_level_json:
            res = self.check_json_key(key, self.res['items'][0])
            to_test = second_level_json[res]

            for item in to_test:
                if res == 'brandingSettings' and self.check_json_key(item, self.res['items'][0][res]['channel']):
                    channel_info[item] = self.res['items'][0][res]['channel'][item]

                elif res == 'contentDetails' and self.check_json_key(item, self.res['items'][0][res]['relatedPlaylists']):
                    channel_info[item] = self.res['items'][0][res]['relatedPlaylists'][item]

                elif self.check_json_key(item, self.res['items'][0][res]):
                    channel_info[item] = self.res['items'][0][res][item]

        self.dictResult([channel_info])

    def uploadVideoList(self, channel_id):
        """
        チャンネルが投稿した動画一覧を取得するメソッド
        :param channel_id: str
        :return: dict {
                    'result':[
                        {
                            'title': title,
                            'id': video_id,
                            'publishTime': publishTime,
                                'description': description
                        },
                    ]
                }
        """
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        URL = 'https://www.googleapis.com/youtube/v3/search'
        payload = {
            'part': 'snippet',
            'channelId': channel_id,
            'key': API_KEY,
            'maxResults': 50,
            'order': 'date'
        }
        r = requests.get(URL, params=payload)
        res = r.json()
        result = []
        items = res['items']
        for item in items:
            title = item['snippet']['title']
            publishTime = item['snippet']['publishTime']
            description = item['snippet']['description']
            video_id = None
            keys = item['id'].keys()
            for key in keys:
                if key == 'videoId':
                    video_id = item['id'][key]
                    video_info = {
                        'title' : title,
                        'id' : video_id,
                        'publishTime' : publishTime,
                        'description' : description
                    }
                    result.append(video_info)
        self.dictResult(result)

    def routine(self):
        self.videoInfo('7BzGOVk0J-s')
        self.channelIdSearch('はじめしゃちょー')
        self.channelInfo('UClKeJXipXwX7_ZGxOBnMQyw')
        self.uploadVideoList('UClKeJXipXwX7_ZGxOBnMQyw')

    def test(self):
        return self.API_KEY


Youtube = Youtube()
Youtube.routine()
