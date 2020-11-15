import requests
import json
from pprint import pprint

def compare_hash_tree(local_json, server_json):
    results = {
        'update': [],
        'add': [],
        'delete': []
    }
    # The client traverses sub folders of the merkle trees,
    # comparing the root hashes of each folder and only continuing in comparison when they mismatch
    for [key_source, value_source], [key_distant, value_distant] in zip(local_json.items(), server_json.items()):
        # a.	Match name, match CRC (hash)
        if key_source == 'path' \
                and key_source == key_distant \
                and value_source == value_distant \
                and local_json['hash'] == server_json['hash']:
            continue

        # b.	Match name, but mismatch CRC (hash)
        if key_source == 'path' \
                and key_source == key_distant \
                and value_source == value_distant \
                and local_json['hash'] != server_json['hash']\
                and 'size' in local_json.keys():
            # adds the file to the change list as an UPDATE action
            results['update'].append(value_source)

        # c.	Mismatch name on server
        if key_source == 'path' and key_source == key_distant:
            # on server
            if value_source and value_source not in server_json['hash']:
                # adds the file to the change list as ADD action
                results['add'].append(value_source)
            # on client
            elif value_distant in server_json['hash'] and value_distant not in local_json['hash']:
                # adds the file to the change list as DELETE action
                results['delete'].append(value_source)
        #TODO  unknown asset exists on server

        if isinstance(value_source, list) and isinstance(value_distant, list):
            continue
            # if value_source:
            #     for d in value_source:
            #         for result in compare_hash_tree(value_source, value_distant):
            #             results.append(result)
            #     else:
            #         print('none')


    return results




def test_platform(platform):
    # root_hash = 'merkleTreeHash.json'
    # connection = requests.get("https://assets.vgas-game.com/{}/Data/{}".format(platform, root_hash))
    # ota_server_curr_root_hash = connection.json()
    #
    # connection.close()
    ota_server_curr_root_hash = open('iphonemerkleTreeHash2.json', "r")
    f2 = open('iphonemerkleTreeHash.json', "r")


    pprint(compare_hash_tree(json.loads(ota_server_curr_root_hash.read()), json.loads(f2.read())))

    f2.close()


platform = 'iphone4'
test_platform(platform)