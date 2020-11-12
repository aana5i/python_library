import boto3
import os
import argparse


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


def prepare_upload(region, endpoint, access_key, secret_access_key, bucket, folder_path, platform, OTA_Version):
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

    # convert the platform name
    # convert_platform = {
    #     "Android": "android_etc",
    #     "IOS": "iphone4",
    #     "MacOS": "macosx"
    # }

    if OTA_Version == 0:
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=region,
                                endpoint_url=endpoint,
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_access_key)

        for root, dirs, files in os.walk(folder_path):
            for name in files:
                # remove the local path before Builds to begin the path by PlatformName/Data
                # current_file = os.path.join(os.path.relpath(root, 'Build'), name)  python3
                current_file = os.path.join(root.split('Build')[1][1:], name)
                print(current_file)
                # take the correct local path
                local_path = os.path.join(root, name)
                if platform in current_file:
                    if 'merkleRootTreeHash.txt' in current_file:
                        client.upload_file(local_path, bucket, current_file, ExtraArgs={'ACL':'public-read'})


def uploader(region, endpoint, access_key, secret_access_key, bucket, folder_path, platform, OTA_Version):
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
    prepare_upload(region, endpoint, access_key, secret_access_key, bucket, folder_path, platform, OTA_Version)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',   '--regionname',         help='S3 server region name. For example: sfo2',                                                required=True)
    parser.add_argument('-e',   '--endpointurl',        help='S3/DigitalOcean endpoint url. For example: https://sfo2.digitaloceanspaces.com/',         required=True)
    parser.add_argument('-k',   '--accesskey',          help='AWS access key',                                                                          required=True)
    parser.add_argument('-s',   '--secretaccesskey',    help='AWS secret access key',                                                                   required=True)
    parser.add_argument('-b',   '--bucketname',         help='S3 bucket name',                                                                          required=True)
    parser.add_argument('-f',   '--fromfolder',         help='File to upload folder path',                                                              required=True)
    parser.add_argument('-t',   '--target',             help='Target platform for conversion',                                                          required=True)
    parser.add_argument('-v',   '--version',            help='OTA version number',                          type=int,                                   required=True)
    args = parser.parse_args()

    # Upload assets
    uploader(args.regionname, args.endpointurl, args.accesskey, args.secretaccesskey, args.bucketname, args.fromfolder, args.target, args.version)



''' USAGE '''
"""
python Uploader.py -r sfo2 -e https://sfo2.digitaloceanspaces.com/ -k key -s secret_key -b bucket_name -f folder_path -t Android -v OTA_version
or 
import Uploader
Uploader.uploader('sfo2', 'https://sfo2.digitaloceanspaces.com/', 'key', 'secret_key', 'bucket_name', 'folder_path', 'Android', 'OTA_version')
"""

