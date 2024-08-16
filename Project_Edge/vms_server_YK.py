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

@ app.route('/')
def index():


    return "접속 완료"

#######

# 엣지 서버 주소 임시 저장용
edge_ip = ""
edge_port = None

# 엣지 서버 연동 정보 교환: VMS - 엣지등록모듈
@ app.route('/edge_info', methods=['POST'])
def set_edge_info():
    edge_info = request.get_json()

    # edge 주소 parsing
    edge_addr_ip = edge_info['ip']
    edge_addr_port = edge_info['port']
    print(edge_addr, edge_port)
    edge_ip = edge_addr_ip
    edge_port = edge_addr_port

    # # edge 연동 인증용 ID/PW
    # edge_auth_id = edge_info['auth_id']
    # edge_auth_pw = edge_info['auth_pw']

    # # 연동가능한 카메라 단말 프로파일 및 분석 종류 정보
    # cam_profile_list = edge_info['cam_list']
    # analysis_type = edge_info['analysis_type']

    res = jsonify(
        code="0000",
        message="엣지 주소 수신 성공",
    )

    return res

#######

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
