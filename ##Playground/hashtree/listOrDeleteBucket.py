import boto3
from config.config import get_credentials
import argparse


BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName = get_credentials()
Ota_client_type = 'oc-ios-en'
file_path = 'merkleRootTreeHash.txt'


def get_connection(region, endpoint, access_key, secret_access_key):
    return boto3.resource('s3',
                        region_name=region,
                        endpoint_url=endpoint,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_access_key)


def list_in_bucket(s3, bucket):
    """
    list all objects from a bucket
    :param s3: boto3 resource object
    :param bucket: str
    :return:
    """
    bucket = s3.Bucket(bucket)
    for o in bucket.objects.filter():
        print(o.key)


def rm_in_bucket(s3, bucket):
    """
    remove all objects from a bucket
    :param s3: boto3 resource object
    :param bucket: str
    :return:
    """
    bucket = s3.Bucket(bucket)
    bucket.objects.all().delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',   '--remove', help='remove all from bucket', action='store_true')
    parser.add_argument('-l',   '--list',   help='list all from bucket',   action='store_true')

    args = parser.parse_args()

    if args:
        s3 = get_connection(BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey)
    if args.list:
        list_in_bucket(s3, BucketName)
    if args.remove:
        rm_in_bucket(s3, BucketName)