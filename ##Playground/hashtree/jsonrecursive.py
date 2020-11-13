import json
import requests



def compare_hash_trees(key, local_json, server_json):
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

    if 'children' in local_json and local_json['children']:
        # for d in local_json['children']:
        for folder, folder2 in zip(local_json['children'], server_json['children']):
            for result in compare_hash_trees(key, folder, folder2):
                results.append(result)

    return results


# def compare_hash_trees(key, local_json, server_json):
#     result = []
#
#     tmp_local = [local_json['path'], local_json['hash']]
#     tmp_server = [server_json['path'], server_json['hash']]
#     if tmp_local[0] != tmp_server[0] or tmp_local[1] != tmp_server[1]:
#         result.append(local_json['path'])
#
#     if 'children' in local_json and local_json['children']:
#         for folder, folder2 in zip(local_json['children'], server_json['children']):
#             for [key, value], [key2, value2] in zip(folder.items(), folder2.items()):
#                 print(key, value, key2, value2)
#                 break
#
#
#
#
#
#
#             # for result in compare_hash_trees(key, child, server_json['children']):
#             #     print(result)
#             # if len(local_json['children']) != len(server_json['children']):
#             #     print(len(local_json['children']) != len(server_json['children']))
#
#
#     return result



def differences(a, b, section = None):
    for [c, d], [h, g] in zip(a.items(), b.items()):
        if not isinstance(d, dict) and not isinstance(g, dict):
            if d != g:
                yield (c, d, g, section)
        elif isinstance(d, list) and isinstance(g, list):
            if d:
                for v in d:
                    for result in differences(v, v):
                        yield result
            else:
                print('none')
        else:
            for i in differences(d, g, c):
                for b in i:
                    yield b




def test_platform(platform):
    root_hash = 'merkleTreeHash.json'
    connection = requests.get(f"https://assets.vgas-game.com/{platform}/Data/{root_hash}")

    # connection = httplib.HTTPSConnection("assets.vgas-game.com", 443, timeout=10)
    # connection.request("GET", "{}/Data/{}".format(platform, root_hash))
    ota_server_curr_root_hash = connection.json()
    connection.close()

    f2 = open('iphonemerkleTreeHash.json', "r")
    # compareParsedJson(ota_server_curr_root_hash, json.loads(f2.read()))
    # print(prepare_path_from_json2('hash', json.loads(f.read())))
    # print(compare_hash_trees('hash', connection.json(), json.loads(f2.read())))
    print(compare_hash_trees('hash', ota_server_curr_root_hash, json.loads(f2.read())))
    # print(list(differences(ota_server_curr_root_hash, json.loads(f2.read()))))

    f2.close()


platform = 'iphone4'
test_platform(platform)
