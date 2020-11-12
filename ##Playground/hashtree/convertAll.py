from HashTree import saveHashTree
from connect3 import uploader


assets_path = 'I:/##LibraryPython/##Playground/DigitalOcean/Users/buildmaster/Jenkins/workspace/Evil01-Branches-VG_Blitz_Trunk/working-copy/ProjectsKindred/Build/android_etc/Data'

get_json = saveHashTree(assets_path)

path_list = get_json

# uploader('sfo2', 'https://sfo2.digitaloceanspaces.com/', 'KMUGUUYSTSKCBQIMRAQQ', 'S92gRsEzqeqrZ0OtamRB5RBB1WkAvbS+tY/tTfpviqgI', 'vgas-ota', 'I:/##LibraryPython/##Playground/DigitalOcean/Users/buildmaster/Jenkins/workspace/Evil01-Branches-VG_Blitz_Trunk/working-copy/ProjectsKindred/Build/android_etc/Data', path_list, 'android_etc', 0)