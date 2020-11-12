#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import json
import sys

CHUNK_SIZE = 4096

def md5(fname):
    """
    md5 hash
    :param fname: str, save file name
    :return: hash_md5 hexdigest
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class Merkle:
    def __init__(self, root_directory):
        self.top_hash = ""
        self.root_directory = root_directory
        self.root = None
        self._initialize_merkle_tree()

    def _initialize_merkle_tree(self):
        """
        initialize the merkle tree
        :return:
        """
        # error check: root directory exist
        if not os.path.isdir(self.root_directory):
            raise Exception("Root path should be a directory")

        # send the directory to the hash func, save created the hash
        self.root = self.create_merkle_node(self.root_directory)
        self.top_hash = self.root.hash

    def create_merkle_node(self, path):
        """
        Create merkle for directory's files
        :param path: str, File or Directory
        :return:
        """

        # error check: file exist
        if os.path.isfile(path):
            size = os.path.getsize(path) if os.path.getsize(path) else 1
            return MerkleNode(md5(path), path, size=size)

        # Path is a directory
        children = []
        hash_str = ""
        # loop on directory's file, create hash, append then
        for file_name in os.listdir(path):
            child_node = self.create_merkle_node(os.path.join(path, file_name))
            hash_str += child_node.hash
            children.append(child_node)

        # return MerkleNode(hashlib.md5(hash_str.encode('utf-8')).hexdigest(), path, children)
        return MerkleNode(hashlib.md5(hash_str.encode('utf-8')).hexdigest(), path, children)


class MerkleNode:
    def __init__(self, hash_code, path, children=None, size=None):
        self.hash = hash_code
        self.path = path.split('Build')[1][1:]  # use only the relative path
        if children:
            self.children = children
        if size:
            self.size = size

class MerkleNodeEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        json encode if not encoded
        :param obj: JSONEncoder obj
        :return: JSONEncoder
        """
        if isinstance(obj, MerkleNode):  # Passe forcement par Merkle ??
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)

def hashTreeForPath(path):
    """
    Launch the Hash process, dump the result in Json
    :param path: str,
    :return:
    """
    merkle = Merkle(path)
    return json.dumps(merkle.root, cls=MerkleNodeEncoder, indent=2)

def saveHashTree(path):
    """
    Launch the Hash process, write the result in Json file
    :param path: str,
    :return:
    """
    _json = hashTreeForPath(path)

    json_path = str(path) + '/merkleTreeHash.json'
    text_path = str(path) + '/merkleRootTreeHash.txt'

    # exclure du tree mais ajouter à l'envoi

    json_data = json.loads(_json)

    with open(json_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)

    with open(text_path, 'w') as outfile:
        outfile.writelines(json_data['hash'])
        outfile.close()

    return json_data

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage: HashTree.py <path>')
    else:
        if len(sys.argv) == 2:
            print(hashTreeForPath(sys.argv[1]))
        elif '-o' in sys.argv:
            saveHashTree(sys.argv[1])

