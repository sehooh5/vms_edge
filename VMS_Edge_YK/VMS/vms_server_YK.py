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

# VMS server IP 주소
ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]
port = "5231"

# host name
user_name = os.getlogin()
print(user_name)

# file path
# file_path = f"/home/{user_name}/"

@ app.route('/index')
def index():
    return render_template('index.html')

#######

### 관리자와의 사전협약 및 등록 단계 획득 정보 ###

# 엣지 서버 접속 정보
edge_server_info = {
    "edge_1": {
        "ip_addr": "192.168.0.21",
        "port": "5231"
    }
}

# VMS 시스템 인증 정보
vms_id = "kim"
vms_pw = "kim123"

# 연동가능 카메라 단말 목록
cam_device_list = ['camera1']
# 연동가능 이벤트 종류
event_list = ['object_detection']
# 인증 암호화 정보
# auth_crypt_info = {
#     "auth_mode": "base" 
# }
#####################################

# 엣지 서버 VMS 인증: VMS - 엣지등록모듈
@ app.route('/edge_user_auth', methods=['POST'])
def request_edge_user_auth():
    edge_req = request.get_json()
    edge_id = edge_req['edge_id']

    # edge 서버 주소
    if edge_id in edge_server_info.keys():
        target_edge_ip = edge_server_info[edge_id]['ip_addr']
        target_edge_port = edge_server_info[edge_id]['port']
        print(target_edge_ip + ":" + target_edge_port)
    else:
        res = jsonify(
            code="400",
            message="EdgeNotExist"
        )

        return res
    
    # VMS user 인증 요청
    url = "http://" + target_edge_ip + ":" + target_edge_port + '/user_auth'
    auth_request = {
        "ID": vms_id,
        "PW": vms_pw
    }
    response = requests.post(url=url, json=auth_request)

    # # 연동가능한 카메라 단말 프로파일 및 분석 종류 정보
    # cam_profile_list = edge_info['cam_list']
    # analysis_type = edge_info['analysis_type']

    return response.json()

# 엣지 카메라 단말 정보 요청

# 엣지 카메라 영상 정보 요청
@ app.route('/cam_stream_info', methods=['POST'])
def request_cam_stream_info():
    stream_req = request.get_json()
    cam_profile_token = stream_req['profile_token']
    stream_setup = stream_req['stream_setup']

    edge_id = 'edge_1'
    target_edge_ip = edge_server_info[edge_id]['ip_addr']
    target_edge_port = edge_server_info[edge_id]['port']
    # 영상 정보 요청
    url = "http://" + target_edge_ip + ":" + target_edge_port + "/stream_info"
    streamUriRequest = {
        "profileToken": cam_profile_token,
        "streamSetup": stream_setup
    }
    response = requests.post(url=url, json=streamUriRequest)

    return response.json()

# 실시간 영상 분석 정보 요청
@ app.route('/realtime_analysis_request', methods=['POST'])
def request_analysis():
    analysis_req = request.get_json()
    cam_profile_token = analysis_req['profile_token']
    duration = analysis_req['duration']

    edge_id = 'edge_1'
    target_edge_ip = edge_server_info[edge_id]['ip_addr']
    target_edge_port = edge_server_info[edge_id]['port']
    # 영상 분석 정보 요청
    url = "http://" + target_edge_ip + ":" + target_edge_port + "/realtime_analysis"
    RealtimeEventRequest = {
        "profileToken": cam_profile_token,
        "duration": duration
    }
    response = requests.post(url=url, json=RealtimeEventRequest)

    return response.json()

# 실시간 영상 분석 정보 수신
@ app.route('/realtime_analysis_endpoint', methods=['POST'])
def handle_result():
    data = request.get_json()
    print("Received results: ", data)

    return jsonify({"status": "success"})
#######

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
