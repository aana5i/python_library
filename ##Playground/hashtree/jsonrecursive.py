import json
import requests


"""
1.	The client connects to the OTA server from the platform’s OTA server info request
2.	The client downloads the merkle tree from that repo
3.	The client traverses sub folders of the merkle trees, comparing the root hashes of each folder and only continuing in comparison when they mismatch
4.	Each folder contains files and subfolders that are sorted; therefore the comparison is O(N), where by the ith data item in each folder should either:
a.	Match name, match CRC (hash), file is ignored
b.	Match name, but mismatch CRC (hash), which adds the file to the change list as an UPDATE action
c.	Mismatch name, unknown asset exists on server, which adds the file to the change list as ADD action
d.	Mismatch name, unknown asset exists on the client, which adds the file to the change list as DELETE action
"""

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
            print(folder)
            for result in compare_hash_trees(key, folder, folder2, server_folder_hash_list):
                results.append(result)

    return results


def test_platform(platform):
    root_hash = 'merkleTreeHash.json'
    connection = requests.get("https://assets.vgas-game.com/{}/Data/{}".format(platform, root_hash))
    ota_server_curr_root_hash = connection.json()

    # connection = httplib.HTTPSConnection("assets.vgas-game.com", 443, timeout=10)
    # connection.request("GET", "{}/Data/{}".format(platform, root_hash))

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