import logging


Log = logging.getLogger('myLogger')
Log.setLevel(9999)

logging.getLogger('Evil.CSLogger').setLevel(9999)
print(logging.DEBUG)
print(Log)

