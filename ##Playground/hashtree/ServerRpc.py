
# -*- coding: iso-8859-15 -*-
import requests
# from config.config import get_credentials
# BucketRegionName, BucketEndpointUrl, BucketKeyId, BucketSecretKey, BucketName = get_credentials()


Ota_client_type = 'oc-android-en'

# add OTa Platform/configure/container.unified.conf
# CDN address, port
# on recupere l'information si c'est un stage ou un live dans le configure

def getServerRootHash(client_type):
    """

    :param client_type:
    :return:
    """

    """
    endpoint_address = Environment.SETTINGS.get('OTA', 'endpoint_address')
    ota_server_port = Environment.SETTINGS.get('OTA', 'ota_server_port')
    root_hash = Environment.SETTINGS.get('OTA', 'root_hash')
    """

    endpoint_address = 'https://assets.vgas-game.com' # from Configure/
    ota_server_port = "443"  #https  # from Configure/
    root_hash = "merkleRootTreeHash.txt"  # from Configure/
    # root_hash = "FE/FEFEE1AF536CB460202E868C6AC63107"  # from Configure/

    # convert the platform name
    convert_platform = {
        "android": "android_etc",
        "ios": "iphone4",
        "macos": "macosx"
    }

    client_type = client_type.split('-')
    platform = convert_platform[client_type[1]]

    # ota_server_url = "{}:{}/vgas-ota/{}/Data/".format(stage_live_endpoint_address, ota_server_port, platform)
    ota_server_url = "{}/{}".format(endpoint_address, platform)

    connection = requests.get(endpoint_address + "/{}/Data/{}".format(platform, root_hash ))

    ota_server_curr_root_hash = connection.text.encode('ascii','ignore')
    connection.close()


    """ BOTO3 version """
    # s3 = boto3.resource('s3',
    #                     region_name=region,
    #                     endpoint_url=endpoint,
    #                     aws_access_key_id=access_key,
    #                     aws_secret_access_key=secret_access_key)
    # bucket = s3.Bucket(bucket)
    #
    # server_root = b'Root Hash ot found'
    # for obj in bucket.objects.all():
    #     if obj.key == file:
    #         server_root = obj.get()['Body'].read()
    # ota_server_curr_root_hash = server_root.decode("utf-8")

    return ota_server_url, ota_server_port, ota_server_curr_root_hash


print(getServerRootHash(Ota_client_type))
