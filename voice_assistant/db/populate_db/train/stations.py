#!/usr/bin/python3
# -*- coding: utf-8 -*-
from pprint import pprint
import urllib.request
import json


with urllib.request.urlopen("http://kamelong.com/API/RosenzuAPI/v0.1/stations") as url:
    data = json.loads(url.read().decode())
    print(data)

