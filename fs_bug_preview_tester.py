###
'''
Whats script does:
- Gets rtsp links from file to list
- Uploads them to fs-api
In cycle with сounter:
- Get stream from fs-api and randomly remove them
- Uploads random stream from list above

Need to set:
- file with rtsp links (one per line)
- streams_counter statement
'''
####

import random, requests, json, re, secrets, time
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
                "luna-account-id": "6d071cca-fda5-4a03-84d5-5bea65904480",
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
FS_URL = "http://192.168.88.200:60001/api/1/streams"
streams_to_remove = []
streams_to_upload = []
streams_counter = 10

def get_streams_from_file_to_list():
    print("Loading streams from file...")
    print()
    time.sleep(2)
    with open('rtsp.txt') as streams:
            for stream in streams:
                streams_to_upload.extend(stream.strip().split('\n'))

def first_time_streams__upload():
    print("First Time Streams Uploading...")
    time.sleep(1)
    for stream in streams_to_upload:
        RTSP_LINK = stream
        camera_ip = "".join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', stream))
        new_camera_config = camera_template['stream-sources'][0]
        new_camera_config['input']['url'] = RTSP_LINK
        new_camera_config['name'] = camera_ip
        new_camera_config = ("[" + "\n" + json.dumps(new_camera_config, indent=4) + "\n" + "]")
        r = requests.post(FS_URL, headers=http_headers, data=new_camera_config)
        print("\t", r.text)
    print()

def remove_random_stream():
    print("\tRemoving Random Stream...")
    time.sleep(1)
    random_streams = []
    current_streams = requests.get(FS_URL)
    current_streams = json.loads(current_streams.text)
    for current_streams in current_streams:
        random_streams.append((current_streams['id']))
    stream_to_remove = secrets.randbelow(len(random_streams))
    stream_to_remove = random_streams[stream_to_remove]
    stream_to_remove = '["' + stream_to_remove + '"]'
    delete_stream = requests.delete(FS_URL, headers=http_headers, data=stream_to_remove)
    print("\t\t", stream_to_remove)

def upload_random_stream():
    time.sleep(1)
    index = random.randrange(len(streams_to_upload)-1)
    RTSP_LINK = streams_to_upload[index]
    camera_ip = "".join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', streams_to_upload[index]))
    new_camera_config = camera_template['stream-sources'][0]
    new_camera_config['input']['url'] = RTSP_LINK
    new_camera_config['name'] = camera_ip
    new_camera_config = ("[" + "\n" + json.dumps(new_camera_config, indent=4) + "\n" + "]")
    r = requests.post(FS_URL, headers=http_headers, data=new_camera_config)
    print("\tUploading Random Stream...")
    print("\t\t", r.text)
    print()


#Main script body
get_streams_from_file_to_list()
first_time_streams__upload()

cnt = 0
while cnt < streams_counter:
    print("====  " + "Cycle Test Counter " + str(cnt) + "  ====")
    remove_random_stream()
    upload_random_stream()
    cnt += 1
