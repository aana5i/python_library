import requests
from pprint import pprint
import urllib.parse
import time
import json

import random


class Youtube:
    def __init__(self):
        self.API_KEY = ['AIzaSyChJkOgioBlWNfQ9k0rDY93cJy530Okok4', 'AIzaSyAy0Im0JhZDw4tcdWXqQhFvEcmyWNCkC10']

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

    def cleanDict(self, key_list, dict):
        return {key: value for (key, value) in dict.items() if key in key_list}

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
        parts = ['snippet', 'contentDetails', 'statistics', 'status']
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
        statistics = res['items'][0]['statistics']

        key_list = ['title', 'publishedAt', 'channelTitle', 'tags', 'description', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount']
        video_info = self.cleanDict(key_list, {**snippet, **statistics})

        self.dictResult([video_info])
        self.channelId = snippet['channelId']

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
                key_list = ['channelTitle', 'channelId']
                channel_info = self.cleanDict(key_list, {**item['snippet'], **item['id']})
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
            # print(json.loads(r.text)['error'])
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
                        'title': title,
                        'id': video_id,
                        'publishTime': publishTime,
                        'description': description
                    }
                    result.append(video_info)
        self.dictResult(result)

    def channelPlayList(self,channel_id):
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        URL = 'https://www.googleapis.com/youtube/v3/playlists'
        parts = ['id','snippet','status']
        part = ','.join([part for part in parts])
        payload = {
            'part': part,
            'channelId': channel_id,
            'key': API_KEY,
            'maxResults': 50
        }
        r = requests.get(URL, params=payload)
        res = r.json()

        items = res['items']
        for item in items:
            print('',':',item['snippet']['title'])
            self.playListVideo(item['id'])

    def playListVideo(self,playlist_id):
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        URL = 'https://www.googleapis.com/youtube/v3/playlistItems'
        #parts = ['snippet','contentDetails','status']
        parts = ['snippet']
        part = ','.join([part for part in parts])
        payload = {
            'part': part,
            'playlistId' : playlist_id,
            'key' : API_KEY,
            'maxResults': 50
        }
        r = requests.get(URL, params=payload)
        res = r.json()

        result = []
        items = res['items']
        for item in items:

            video_info = {
                'id': item['snippet']['resourceId']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'publishedAt': item['snippet']['publishedAt']
            }
            result.append(video_info)
        self.dictResult(result)

    def searchQuery(self,query):
        API_KEY = self.API_KEY[random.randrange(len(self.API_KEY))]
        URL = 'https://www.googleapis.com/youtube/v3/search'
        parts = ['snippet']
        part = ','.join([part for part in parts])
        payload = {
            'part' : part,
            'q' : query,
            'key' : API_KEY,
            'maxResults': 50
        }
        r = requests.get(URL, params=payload)
        res = r.json()

        result = []
        items = res['items']
        for item in items:
            for k in item['id']:
                if 'videoId' in k:
                    #print(item['id']['videoId'])
                    search_video_info = {
                        'id' : item['id']['videoId'],
                        'title' : item['snippet']['title']
                    }
                    result.append(search_video_info)
        #self.dictResult(result)

        pprint(result)
        vi = ""
        #voice
        video_title = input("動画のタイトル")
        for r in result:
            if r['title'] == video_title:
                vi = r['id']
        self.videoId = vi

    def routine(self, query):
        # self.videoInfo('7BzGOVk0J-s')
        # self.channelIdSearch('はじめしゃちょー')
        # self.channelInfo(channel_id)
        # self.uploadVideoList('UClKeJXipXwX7_ZGxOBnMQyw')
        self.searchQuery(query)
        self.videoInfo(self.videoId)
        print(self.channelId)
        self.channelPlayList(self.channelId)

    def test(self):
        return self.API_KEY


if __name__ == '__main__':
    Youtube = Youtube()
    Youtube.routine('UClKeJXipXwX7_ZGxOBnMQyw')
