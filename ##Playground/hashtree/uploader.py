import boto3
import os
import argparse
from config.config import get_credentials


BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName = get_credentials()

path = 'I:\\Nouveau dossier'

def uploader(region, endpoint, access_key, secret_access_key, bucket, folder_path, OTA_Version):
    if OTA_Version == 0:
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=region,
                                endpoint_url=endpoint,
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_access_key)

        for filename in os.scandir(folder_path):
            # Build path
            local_path = os.getcwd()
            local_name = os.path.join(local_path, folder_path)
            if os.path.isdir(filename):
                # Create a folder on bucket
                # client.put_object(Bucket=s3_bucket, Key=filename.name + '/')  # Android, IOS
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


uploader(BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName, path, 0)
