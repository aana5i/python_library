import boto3

import os
from pprint import pprint
from botocore.client import Config


def boto_version():
    # Initialize a session using DigitalOcean Spaces.
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='sfo2',
                            endpoint_url='https://sfo2.digitaloceanspaces.com/',
                            aws_access_key_id='ASTYZ2ETKHIUWXQ2NT6L',
                            aws_secret_access_key='PRNn5Am8sTfcVyWNmgcEonc5+bATq7UIcqHhkd3qkh0')
    #  %(bucket)s.sfo2.digitaloceanspaces.com

    # List all buckets on your account.
    response = client.list_buckets()

    spaces = [space['Name'] for space in response['Buckets']]
    print("Spaces List: %s" % spaces)

    # client.upload_file('first note.json',
    #                    'taskbook',
    #                    'open-api-static/task/first_note.json'
    #                    'private')

    s3_bucket = 'taskbook'

    folder = 'up'
    for filename in os.scandir(folder):

        local_path = os.getcwd()
        local_name = os.path.join(local_path, folder)

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

                        client.upload_file(current_nested_file, s3_bucket, current_nested_folder)

                else:
                    # Build the current folder path !!! don't use os.path.join()
                    current_file = local_name + '/' + current_folder
                    client.upload_file(current_file, s3_bucket, current_folder)

    # upload
    file = folder + '/' + 'first note.json'
    bucket_file_name = 'first_note.json'
    client.upload_file(file, s3_bucket, bucket_file_name)

boto_version()
