#!/usr/bin/env python
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
import os
import response
import string
import random
import paramiko
import time
import subprocess
import datetime
import sys


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# # 다른 서버에 명령 보낼때 사용
# cli = paramiko.SSHClient()
# cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# # 랜덤한 문자열 생성기
# _LENGTH = 4
# string_pool = string.ascii_letters + string.digits

# API_URL = "http://123.214.186.244:4880"

# IP 주소
ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]
port = "5231"

# host name
user_name = os.getlogin()
print(user_name)

# file path
# file_path = f"/home/{user_name}/"

@ app.route('/')
def index():


    return "접속 완료"

#######
# (예시) vms 유저 정보
user_list = ["keti", "kim"]
user_info_dict = {
    "keti": {
        "password": "keti123",
        "userInfo": {
            "userName": "keti",
            "userLevel": "Administrator"
        }
    },
    "kim": {
        "password": "kim123",
        "userInfo": {
            "userName": "kim",
            "userLevel": "Operator"
        }
    }
}
# 시스템 간 인증 요청 응답: 엣지 - VMS
@ app.route('/auth_req', methods=['POST'])
def check_auth():
    AuthenticationRequest = request.get_json()

    # 사용자 인증 정보 parsing
    id_req = AuthenticationRequest['ID']
    pw_req = AuthenticationRequest['PW']
    print(id_req, pw_req)

    if id_req in user_list:
        if pw_req == user_info_dict[id_req]['password']:
            res = jsonify(
                code="0000",
                message="AuthenticationResponse",
                userInfo=user_info_dict[id_req]['userInfo']
            )
        else:
            res = jsonify(
                code="1111",
                message="AuthenticationFail",
            )
    else:
        res = jsonify(
            code="1111",
            message="AuthenticationFail",
        )

    return res

# (예시) 카메라 단말 프로파일 정보
profiles = ["cam_1_token", "cam_1_profile"]
# 카메라 단말 프로파일 요청 응답: 엣지 - VMS
@ app.route('/profiles', methods=['GET'])
def send_cam_profiles():
    
    res = jsonify(
        code="0000",
        message="ProfilesResponse",
        profiles=profiles
    )
    
    return res

# (예시) 카메라 단말 부가정보
device_info = {
    "deviceName": "camera1",
    "deviceType": "Wired_PTZ"
}
# 카메라 단말 부가정보 요청 응답: 엣지 - VMS
@app.route('/device_info', methods=['POST'])
def send_device_info():
    VideoDeviceInfoRequest = request.get_json()

    # 카메라 단말 프로필 토큰
    token = VideoDeviceInfoRequest['profileToken']
    print(token)

    if token == profiles[0]:
        res = jsonify(
            code="0000",
            message="VideoDeviceInfoResponse",
            deviceInfo=device_info
        )
    else:
        res = jsonify(
            code="1111",
            message="DeviceNotExist",
        )
    
    return res

# (예시) 카메라 영상 정보
stream_base = "192.168.0.76/"
# 카메라 단말 영상정보 요청 응답: 엣지 - VMS
@app.route('/stream_info', methods=['POST'])
def send_video_info():
    StreamUriRequest = request.get_json()

    # 카메라 단말 프로필 토큰
    token = StreamUriRequest['profileToken']
    # 영상 전송 설정
    stream_setup = StreamUriRequest['streamSetup']
    print(token)
    print(stream_setup)

    if token == profiles[0]:
        uri = stream_base + stream_setup['stream'] + '/' + stream_setup['protocol']

        res = jsonify(
            code="0000",
            message="StreamUriResponse",
            URI=uri
        )
    else:
        res = jsonify(
            code="1111",
            message="DeviceNotExist",
        )
    
    return res

# (예시) 영상 분석 정보
analyzed_events = {
    "deviceName": "camera1",
    "eventDataList": {
        "eventID": "event01",
        "eventName": "넘어짐",
        "startTime": "2024-08-09 17:59:00",
        "duration": "1280"
    }
}
# 실시간 영상 분석 정보 요청 응답: 엣지 - VMS
@app.route('/realtime_events', methods=['POST'])
def send_realtime_events():
    RealtimeEventRequest = request.get_json()

    # 카메라 단말 프로필 토큰
    token = RealtimeEventRequest['profileToken']
    # 연동 지속 시간
    duration = RealtimeEventRequest['duration']
    print(token, duration)

    if token == profiles[0]:

        res = jsonify(
            code="0000",
            message="RealtimeEventResponse",
            events=analyzed_events
        )
    else:
        res = jsonify(
            code="1111",
            message="DeviceNotExist",
        )
    
    return res
#######

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
