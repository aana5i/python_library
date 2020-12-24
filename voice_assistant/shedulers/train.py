#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
print('shedulers: train')
subprocess.call(["python3", "service_chooser.py", "-tr", "infos"], cwd=r"/var/www/prog/")

