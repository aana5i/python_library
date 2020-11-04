import boto3
from config.config import get_credentials
BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName = get_credentials()
Ota_client_type = 'oc-ios-en'


''' need boto3 '''
def selectCorrectHashTree(region, endpoint, access_key, secret_access_key, bucket, client_type, OTA_Version):

    region_endpoint_address = {'sa': 'http://10.10.10.10', 'oc': 'http://12.12.12.12'}
    region_endpoint_port = {'ios': '1234', 'android': '3030'}  #comment on choisit le port, est ce bien en fonction de la platform client ?

    # if client_rootHash == server_rootHash:
    #     return  True

    client_type = client_type.split('-')
    ota_server_url = region_endpoint_address[client_type[0]]\
                     + ':'\
                     + region_endpoint_port[client_type[1]]\
                     + '/assets/'\
                     + client_type[1]\
                     + '/'\
                     + client_type[2]
    ota_server_port = region_endpoint_port[client_type[1]]
    ''' on renvoi le port dans l'url et ensuite dans ota_server_port ?? '''

    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=region,
                            endpoint_url=endpoint,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_access_key)
    client.download_file(bucket, 'merkleRootTreeHash.txt', '/merkleRootTreeHash.txt')
    server_root = open("merkleRootTreeHash.txt", "r")
    server_rootHash = server_root.read()
    server_root.close()
    ota_server_curr_root_hash = server_rootHash

    return ota_server_url, ota_server_port, ota_server_curr_root_hash


print(selectCorrectHashTree(BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName, Ota_client_type, 0))
