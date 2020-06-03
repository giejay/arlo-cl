from arlo import Arlo
import sys
import os
import errno
import configparser
import base64
from subprocess import call
import time

configfile = "arlo-cl.cfg"

# Initialize config file
if not os.path.isfile(configfile):
    print("Error: Config file "+configfile+" not found" )
    sys.exit(errno.ENOENT)
config = configparser.ConfigParser()
config.read(configfile)

# Credentials for Arlo
USERNAME = config.get("CREDENTIALS","USERNAME")
PASSWORD = str(base64.b64encode(config.get("CREDENTIALS","PASSWORD").encode("utf-8")), "utf-8")

# Base Station (currently only one base station supported!)
BASESTATIONNAME = config.get("BASESTATION","NAME")

# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
# Subsequent successful calls to login will update the oAuth token.
arlo = Arlo(USERNAME, PASSWORD)

devices = arlo.GetDevices('camera')

arlo.Subscribe(devices[0])

url = arlo.StartStream(devices[0], devices[0])

print(url)

# call(['ffmpeg',  '-v', 'verbose', '-i', url, '-c:v', 'libx264', '-c:a', 'aac' '-ac', '1', '-strict', '-2', '-crf', '18', '-profile:v', 'baseline', '-maxrate', '400k', '-start_number', '1', 'stream.m3u8'])

call(['ffmpeg','-i',url,'-r','100','-crf','25','-preset','faster','-maxrate','500k','-bufsize','1500k','-c:v','libx264','-hls_time','4','-hls_list_size','2','-hls_wrap','2','-start_number','1','-y','playlist.m3u8'])

# call(['ffmpeg', '-y', '-re', '-i', url, '-t', '10', '-acodec', 'copy', '-vcodec', 'copy', str(round(time.time() * 1000)) + '.mp4'])
