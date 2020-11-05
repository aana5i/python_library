import boto3
import os
from config.config import get_credentials


BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName = get_credentials()


class AwsConnect:
    def __init__(self):
        pass

    def get_connection(self, BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey):
        # Initialize a session using DigitalOcean Spaces.
        session = boto3.session.Session()
        self.client = session.client('s3',
                                     region_name=BucketRegionName,
                                     endpoint_url=BucketEndpointUrl,
                                     aws_access_key_id=BucketKeyId,
                                     aws_secret_access_key=BucketSecretKey)

    def list_all_buckets(self):
        # List all buckets on your account.
        response = self.client.list_buckets()

        spaces = [space['Name'] for space in response['Buckets']]
        print("Spaces List: %s" % spaces)

    def upload_file(self, BucketName, folderPath):
        s3_bucket = BucketName

        folder = folderPath
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

                            self.client.upload_file(current_nested_file, s3_bucket, current_nested_folder)

                    else:
                        # Build the current folder path !!! don't use os.path.join()
                        current_file = local_name + '/' + current_folder

                        self.client.upload_file(current_file, s3_bucket, current_folder)
            else:
                # upload root files
                file = folder + '/' + filename.name
                bucket_file_name = filename.name
                self.client.upload_file(file, s3_bucket, bucket_file_name)



aws = AwsConnect()
aws.get_connection(BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey)
aws.list_all_buckets()
aws.upload_file(BucketName, 'up')