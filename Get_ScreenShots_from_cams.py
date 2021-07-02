#!/usr/bin/python3

"""
###########################################################
Python 3.7+
Script gets cameras from FaceStream API and saves them to
screenshots (jpg) with camera_name ("name") as name.
Please set FS_API
Probably need install Pillow lib instead of PIL
###########################################################
"""

import requests, json, urllib.request, time, io
import _thread as thread
from PIL import Image

FS_IP = "http://192.168.151.168:60001"
FS_API_URL = "{}/api/1/streams".format(FS_IP)

start_time = time.time()
streams = requests.get(FS_API_URL)
streams = json.loads(streams.text)
cameras = []

for stream in streams:
    cameras.append(((stream['id']), (FS_IP + stream['preview_url']), stream['name']))

def getImage(imgStream):
    print('Starting getimage')
    bytes = b''
    counter = 0
    start_time = time.time()
    while counter < 1:
        bytes += imgStream.read(1024)
        # Find the beginning / end of an JPG file
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        # Check if we actually got any bytes
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            file = io.BytesIO(jpg)
            thread.start_new_thread(saveImage,(file, counter))
            counter += 1
            time.sleep(0.5)

def saveImage(ImageBytes, fileCount):
    elapsed_time = time.time() - start_time
    fileName = "{}.jpg".format(camera_name)
    img = Image.open(ImageBytes)
    img.save(fileName)
    print(fileName + " was saved | " + str(elapsed_time))

for cam in cameras:
    camera_id = (cam[0])
    preview_url = (cam[1])
    camera_name = (cam[2])
    imageStream = urllib.request.urlopen(preview_url)
    getImage(imageStream)
