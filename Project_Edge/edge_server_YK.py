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
# user_list = ["root", "kim"]
user_info_dict = {
    "root": {
        "password": "keti",
        "userInfo": {
            "userName": "root",
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
@ app.route('/user_auth', methods=['POST'])
def check_auth():
    AuthenticationRequest = request.get_json()

    # 사용자 인증 정보 parsing
    id_req = AuthenticationRequest['ID']
    pw_req = AuthenticationRequest['PW']
    print(id_req, pw_req)

    if id_req in user_info_dict.keys():
        if pw_req == user_info_dict[id_req]['password']:
            res = jsonify(
                code="200",
                message="OK",
                userInfo=user_info_dict[id_req]['userInfo']
            )
        else:
            res = jsonify(
                code="400",
                message="AuthenticationFail",
            )
    else:
        res = jsonify(
            code="400",
            message="AuthenticationFail",
        )

    return res

# (예시) 카메라 단말 프로파일 정보
profiles = [{
    "profileToken": "cam_1_token",
    "profileName": "cam_1_profile"
}]
# 카메라 단말 프로파일 요청 응답: 엣지 - VMS
@ app.route('/profiles', methods=['GET'])
def send_cam_profiles():
    
    res = jsonify(
        code="200",
        message="OK",
        profiles=profiles
    )
    
    return res

# (예시) 카메라 단말 부가정보
device_info = {
    "deviceName": "camera1",
    "deviceType": "Wired_PTZ"
}
# 카메라 단말 부가정보 요청 응답: 엣지 - VMS
@ app.route('/device_info', methods=['POST'])
def send_device_info():
    VideoDeviceInfoRequest = request.get_json()

    # 카메라 단말 프로필 토큰
    token = VideoDeviceInfoRequest['profileToken']
    print(token)

    if token == profiles[0]['profileToken']:
        res = jsonify(
            code="200",
            message="OK",
            deviceInfo=device_info
        )
    else:
        res = jsonify(
            code="400",
            message="TokenNotFound",
        )
    
    return res

# (예시) 카메라 영상 취득 경로 정보
stream_addr = "192.168.0.93/onvif-media/media.amp"
user_id = "root"
user_pw = user_info_dict[user_id]['password']
# 카메라 단말 영상정보 요청 응답: 엣지 - VMS
@ app.route('/stream_info', methods=['POST'])
def send_stream_info():
    StreamUriRequest = request.get_json()

    # 카메라 단말 프로필 토큰
    token = StreamUriRequest['profileToken']
    # 영상 전송 설정
    stream_setup = StreamUriRequest['streamSetup']
    print(token)
    print(stream_setup)

    if token == profiles[0]['profileToken']:
        uri = stream_setup['protocol'] + '://' + user_id + ":" + user_pw + "@" + stream_addr

        res = jsonify(
            code="200",
            message="OK",
            URI=uri
        )
    else:
        res = jsonify(
            code="400",
            message="TokenNotFound",
        )
    
    return res

# 실시간 영상 분석 정보 요청 응답: 엣지 - VMS
@ app.route('/realtime_analysis', methods=['POST'])
def send_realtime_events():
    RealtimeEventRequest = request.get_json()

    # 카메라 단말 프로필 토큰
    token = RealtimeEventRequest['profileToken']
    # 연동 지속 시간
    # duration = RealtimeEventRequest['duration']
    print(token)

    analyses = []

    if token == profiles[0]['profileToken']:
        analysis = dict()
        analysis['deviceName'] = profiles[0]['profileName']

        # 최신 kitti result 파일명 확인 command
        cmd = "ls -tr | tail -1"
        # detection 결과 저장 위치
        cwd = "/home/ykkim/workspace/DeepStream-Yolo/kitti_outputs/"
        proc = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        result_filename = proc.stdout.readline().strip()

        print(result_filename)
        objectDataList = []
        idx = 0
        with open(cwd + result_filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                tmp = line.strip().split()
                objectData = dict()
                objectData['objectID'] = "object" + str(idx)
                objectData['objectType'] = tmp[0]
                # left, top, right, bottom
                objectData['bbox'] = [tmp[4], tmp[5], tmp[6], tmp[7]]
                objectData['confidence'] = tmp[15]
                idx+=1
                objectDataList.append(objectData)
        analysis['analysisDataList'] = objectDataList

        analyses.append(analysis)
        res = jsonify(
            code="200",
            message="OK",
            analyses=analyses
        )
    else:
        res = jsonify(
            code="400",
            message="TokenNotFound",
        )
    
    return res
#######

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
