import json
import requests
import httplib


def compare_hash_trees(key, local_json, server_json):  # to_send, already_in_bucket
    """
    recursively compare local and server json
    :param key: str  'path'
    :param json: json Object
    :return: list
    """
    results = []

    if key not in server_json:
        results.append(local_json['path'].encode('utf-8'))
    elif local_json[key] != server_json[key]:

        results.append(local_json['path'].encode('utf-8'))
    if 'children' in local_json.keys():
        if local_json['children']:
            for counter, d in enumerate(local_json['children']):
                for result in compare_hash_trees(key, d, server_json['children'][counter]):
                    results.append(result)

    return results

'''
requests version
'''
# connection = requests.get("https://assets.vgas-game.com/android_etc/Data/merkleTreeHash.json")


platform = 'android_etc'
root_hash = 'merkleTreeHash.json'
connection = httplib.HTTPSConnection("assets.vgas-game.com", 443, timeout=10)
connection.request("GET", "{}/Data/{}".format(platform, root_hash))
ota_server_curr_root_hash = connection.getresponse().read()
connection.close()

f2 = open('merkleTreeHash2.json', "r")

# print(prepare_path_from_json2('hash', json.loads(f.read())))
# print(compare_hash_trees('hash', connection.json(), json.loads(f2.read())))
print(compare_hash_trees('hash', json.loads(ota_server_curr_root_hash), json.loads(f2.read())))


f2.close()