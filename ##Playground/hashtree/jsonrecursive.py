import json
import requests



def compare_hash_trees(key, local_json, server_json, server_folder_hash_list=None):
    """
    recursively compare local and server json
    :param key: str
    :param local_json: jsonObject
    :param server_json: jsonObject
    :param server_folder_hash_list: List => str
    :return:
    """
    results = []

    # if we are on a folder, we use a list of all the server's hash on this folder
    if server_folder_hash_list:
        server_json[key] = server_folder_hash_list

    # only send the file path in bucket, never send the folder
    if 'size' in local_json:
        # case: the file is not present on the server
        if key not in server_json:
            results.append(local_json['path'].encode('utf-8'))

        # case: the file is different on the server
        elif local_json[key] not in server_json[key]:
            results.append(local_json['path'].encode('utf-8'))

    # folder
    if 'children' in local_json and local_json['children']:
        # create the folder hash list
        server_folder_hash_list = [hash['hash'] for hash in server_json['children']]
        # zip the current json and send the hash list
        for folder, folder2 in zip(local_json['children'], server_json['children']):
            for result in compare_hash_trees(key, folder, folder2, server_folder_hash_list):
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
