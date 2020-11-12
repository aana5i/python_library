import boto3
import os
import json
import argparse


def prepare_path_from_json(key, json):
    """
    take all path keys from the merklehashtree
    :param key: str  'path'
    :param json:
    :return:
    """
    results = []
    for k, v in json.items():
        if k == key and 'size' in json.keys():
            results.append(v)
        if isinstance(v, dict):
            for result in prepare_path_from_json(key, v):
                results.append(result)
        elif isinstance(v, list):
            if v:
                for d in v:
                    for result in prepare_path_from_json(key, d):
                        results.append(result)
            else:
                print('none')
    return results

def prepare_bucket(region, endpoint, access_key, secret_access_key, bucket):
    """
    set bucket permission to public
    :param region: str                  sfo2
    :param endpoint: str                https://sfo2.digitaloceanspaces.com/
    :param access_key: str              key
    :param secret_access_key: str       private key
    :param bucket: str                  vgas-ota
    :return:
    """
    s3 = boto3.resource('s3',
                        region_name=region,
                        endpoint_url=endpoint,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_access_key)

    object = s3.Bucket(bucket)
    object.Acl().put(ACL='private')


def prepare_upload(region, endpoint, access_key, secret_access_key, bucket, folder_path, json, platform, OTA_Version):
    """
    upload assets
    :param region: str                  sfo2
    :param endpoint: str                https://sfo2.digitaloceanspaces.com/
    :param access_key: str              key
    :param secret_access_key: str       private key
    :param bucket: str                  vgas-ota
    :param folder_path: str             ..../Builds/PlatformName/Data/
    :param platform: str                android_etc / iphone4 / macosx
    :param OTA_Version: int             0
    :return:
    """

    if OTA_Version == 0:
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=region,
                                endpoint_url=endpoint,
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_access_key)


        path_list = prepare_path_from_json('path', json)
        for path in list(path_list):
            local_path = "{}{}".format(folder_path.split(platform)[0], path)
            current_file = path
            if platform in current_file:
                print(local_path, current_file)
                # client.upload_file(local_path, bucket, current_file, ExtraArgs={'ACL':'public-read'})
        merkleHeahTree = ['merkleTreeHash.json', 'merkleRootTreeHash.txt']
        for hashFile in merkleHeahTree:
            print("{}{}".format(folder_path, hashFile))


def uploader(region, endpoint, access_key, secret_access_key, bucket, folder_path, json, platform, OTA_Version):
    """
    upload asset routine, set the bucket permission and upload assets
    :param region: str                  sfo2
    :param endpoint: str                https://sfo2.digitaloceanspaces.com/
    :param access_key: str              key
    :param secret_access_key: str       private key
    :param bucket: str                  vgas-ota
    :param folder_path: str             ..../Builds/PlatformName/Data/
    :param platform: str                Android
    :param OTA_Version: int             0
    :return:
    """
    # prepare_bucket(region, endpoint, access_key, secret_access_key, bucket)
    prepare_upload(region, endpoint, access_key, secret_access_key, bucket, folder_path, json, platform, OTA_Version)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',   '--regionname',         help='S3 server region name. For example: sfo2',                                                required=True)
    parser.add_argument('-e',   '--endpointurl',        help='S3/DigitalOcean endpoint url. For example: https://sfo2.digitaloceanspaces.com/',         required=True)
    parser.add_argument('-k',   '--accesskey',          help='AWS access key',                                                                          required=True)
    parser.add_argument('-s',   '--secretaccesskey',    help='AWS secret access key',                                                                   required=True)
    parser.add_argument('-b',   '--bucketname',         help='S3 bucket name',                                                                          required=True)
    parser.add_argument('-f',   '--fromfolder',         help='File to upload folder path',                                                              required=True)
    parser.add_argument('-j',   '--json',               help='File to upload relative folder path',                                                     required=True)
    parser.add_argument('-t',   '--target',             help='Target platform for conversion',                                                          required=True)
    parser.add_argument('-v',   '--version',            help='OTA version number',                          type=int,                                   required=True)
    args = parser.parse_args()

    # Upload assets
    uploader(args.regionname, args.endpointurl, args.accesskey, args.secretaccesskey, args.bucketname, args.fromfolder, args.json, args.target, args.version)



''' USAGE '''
"""
python Uploader.py -r sfo2 -e https://sfo2.digitaloceanspaces.com/ -k key -s secret_key -b bucket_name -f folder_path -j jsonObject -t Android -v OTA_version
or 
import Uploader
Uploader.uploader('sfo2', 'https://sfo2.digitaloceanspaces.com/', 'key', 'secret_key', 'bucket_name', 'folder_path', 'jsonObject', 'Android', 'OTA_version')
"""

