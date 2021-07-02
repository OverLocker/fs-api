"""
Python 3.8+

FaceStream configs generator / uploader
Gets rtsp links and name from file (";" as delimiter)

Need to set:
- FS_URL (from 1 to unlimited)
- Output_URL
- Luna_Account_ID

Check input file before run script:
- One link per line
- No spaces
- No unexpected symbols
- Other impossible things
"""

import json, requests, re

input_file = 'additional_list.txt'

camera_template = dict(json.loads(json.dumps({
    "stream-sources": [
        {
            "name": "stream_0",
            "input": {
                "roi": [0, 0, 0, 0],
                "droi": [0, 0, 0, 0],
                "rotation": 0,
                "transport": "tcp",
                "url": "rtsp://some_stream_address",
                "numberOfFfmpegThreads": 0,
                "frame-processing-mode": "auto"
            },
            "output": {
                "login": "loginExample",
                "password": "passwordExample",
                "token": "deadbeef-0000-1111-2222-deadbeef0000",
                "luna-account-id": "62a28f5c-cb84-44c8-8f3b-045e562c88bc",
                "url": "https://127.0.0.1/super_server/",
                "image_store_url": "https://127.0.0.1/super_server/"
            },
            "filtering": {
                "min-score": 0.5187,
                "detection-yaw-threshold": 40,
                "detection-pitch-threshold": 40,
                "detection-roll-threshold": 30,
                "yaw-number": 1,
                "yaw-collection-mode": False,
                "mouth-occlusion-threshold": 0.0
            },
            "sending": {
                "time-period-of-searching": -1,
                "silent-period": 0,
                "type": "sec",
                "number-of-bestshots-to-send": 1
            },
            "health_check": {
                "max_error_count": 10,
                "period": 3600,
                "retry_delay": 5
            },
            "primary_track_policy": {
                "use_primary_track_policy": False,
                "best_shot_min_size": 70,
                "best_shot_proper_size": 140
            },
            "liveness": {
                "use_shoulders_liveness_filtration": False,
                "use_mask_liveness_filtration": False,
                "use_flying_faces_liveness_filtration": False,
                "liveness_mode": 1,
                "number_of_liveness_checks": 10,
                "liveness_threshold": 0.8,
                "livenesses_weights": [0.05, 0.45, 0.5],
                "mask_backgrounds_count": 300
            }
        }
    ]
})))
http_headers = {'Content-Type': 'Application/json'}

FS_URLS = ["http://192.168.151.168:60001/api/1/streams"

           ]

fs_counter = 0

Luna_Account_ID = "6d071cca-fda5-4a03-84d5-5bea65904480"
Output_URL = "http://127.0.0.1:5130/handlersssss"

with open(input_file) as file:
    for rtsp in file:
        if fs_counter < len(FS_URLS):
            camera_attr = rtsp.split(";")
            RTSP_LINK = camera_attr[0].strip()
            camera_name = camera_attr[1].strip()
            camera_ip = "".join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', RTSP_LINK))
            new_camera_config = camera_template['stream-sources'][0]
            new_camera_config['input']['url'] = RTSP_LINK
            new_camera_config['name'] = camera_name
            new_camera_config['output']['url'] = Output_URL
            new_camera_config['output']['luna-account-id'] = Luna_Account_ID
            new_camera_config = ("[" + "\n" + json.dumps(new_camera_config, indent=4) + "\n" + "]")
            #request = requests.post(FS_URLS[fs_counter], data=new_camera_config, headers=http_headers)
            #print(request.text)
            #print(fs_counter)
            print(camera_name)
            fs_counter += 1
        else:
            fs_counter = 0
            #request = requests.post(FS_URLS[fs_counter], data=new_camera_config, headers=http_headers)
            # print(request.text)
            #print(fs_counter)
            print(camera_name)
            fs_counter = 1
