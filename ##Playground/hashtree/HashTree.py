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
    if isinstance(fname, str):
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                hash_md5.update(chunk)
    else:
        hash_md5.update(fname)
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
            return MerkleNode(md5(path), path)
        
        # Path is a directory
        children = []
        hash_str = ""
        # loop on directory's file, create hash, append then
        for file_name in os.listdir(path):
            child_node = self.create_merkle_node(os.path.join(path, file_name))
            hash_str += child_node.hash
            children.append(child_node)
        # return MerkleNode(hashlib.md5(hash_str.encode('utf-8')).hexdigest(), path, children)
        return MerkleNode(md5(hash_str.encode('utf-8')), path, children)


class MerkleNode:
    def __init__(self, hash_code, path, children=None):
        self.hash = hash_code
        self.path = path
        self.children = children


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


# TODO save the JSON
def hashTreeForPath(path):
    """
    Launch the Hash process, dump the result in Json
    :param path: str,
    :return:
    """
    merkle = Merkle(path)
    return json.dumps(merkle.root, cls=MerkleNodeEncoder, indent=2)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage: HashTree.py <path>')
    else:
        print(hashTreeForPath(sys.argv[1]))
