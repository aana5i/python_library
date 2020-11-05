import boto3
from config.config import get_credentials


BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName = get_credentials()
Ota_client_type = 'oc-ios-en'
file_path = 'merkleRootTreeHash.txt'


def find_file_bucket(region, endpoint, access_key, secret_access_key, bucket, file_path, OTA_Version):
    if OTA_Version == 0:
        s3 = boto3.resource('s3',
                            region_name=region,
                            endpoint_url=endpoint,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_access_key)
        bucket = s3.Bucket(bucket)

        for obj in bucket.objects.all():
            if obj.key == file_path:
                body = obj.get()['Body'].read()
                print(body.decode("utf-8") )




find_file_bucket(BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName, file_path, 0)
