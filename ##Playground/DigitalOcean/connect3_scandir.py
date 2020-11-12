import boto3
import os
import argparse


def uploader(region, endpoint, access_key, secret_access_key, bucket, folder_path, OTA_Version):
    if OTA_Version == 0:
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=region,
                                endpoint_url=endpoint,
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_access_key)

        for filename in os.scandir(folder_path):
            print(filename)
            # Build path
            local_path = os.getcwd()
            local_name = os.path.join(local_path, folder_path)
            if os.path.isdir(filename):
                for _filename in os.scandir(filename):
                    # Build the current folder path !!! don't use os.path.join()
                    current_folder = filename.name + '/' + _filename.name
                    if os.path.isdir(_filename):
                        for __filename in os.scandir(_filename):
                            # Build the current folder/file path !!! don't use os.path.join()
                            current_nested_folder = current_folder + '/' + __filename.name
                            current_nested_file = local_name + '/' + current_nested_folder
                            # upload the files, (local_file_path_to_upload, bucket_name, distant_file_path
                            client.upload_file(current_nested_file, bucket, current_nested_folder)
                    else:
                        # Build the current folder path !!! don't use os.path.join()
                        current_file = local_name + '/' + current_folder
                        # upload the files, (local_file_path_to_upload, bucket_name, distant_file_name
                        client.upload_file(current_file, bucket, current_folder)
            else:
                # upload root files
                file = folder_path + '/' + filename.name
                bucket_file_name = filename.name
                client.upload_file(file, bucket, bucket_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',   '--regionname',         help='S3 server region name. For example: sfo2',                                                required=True)
    parser.add_argument('-e',   '--endpointurl',        help='S3/DigitalOcean endpoint url. For example: https://sfo2.digitaloceanspaces.com/',         required=True)
    parser.add_argument('-k',   '--accesskey',          help='AWS access key',                                                                          required=True)
    parser.add_argument('-s',   '--secretaccesskey',    help='AWS secret access key',                                                                   required=True)
    parser.add_argument('-b',   '--bucketname',         help='S3 bucket name',                                                                          required=True)
    parser.add_argument('-f',   '--fromfolder',         help='File to upload folder path',                                                              required=True)
    parser.add_argument('-v',   '--version',            help='OTA version number',                          type=int,                                   required=True)
    args = parser.parse_args()

    # Upload assets
    uploader(args.regionname, args.endpointurl, args.accesskey, args.secretaccesskey, args.bucketname, args.fromfolder, args.version)



''' USAGE '''
"""
python Uploader.py -r sfo2 -e https://sfo2.digitaloceanspaces.com/ -k key -s secret_key -b bucket_name -f folder_path -v OTA_version
or 
import Uploader
Uploader.uploader('sfo2', 'https://sfo2.digitaloceanspaces.com/', 'key', 'secret_key', 'bucket_name', 'folder_path', 'OTA_version')
"""