#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import response


# # sudo 사용으로 k8s config 설정 파일 위치 지정해주기
# os.environ['KUBECONFIG'] = '/home/edge-master-01/.kube/config'
#
# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
# CORS(app)
#
# # 다른 서버에 명령 보낼때 사용
# cli = paramiko.SSHClient()
# cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#
# # 랜덤한 문자열 생성기
# _LENGTH = 4
# string_pool = string.ascii_letters + string.digits
#
# API_URL = "http://123.214.186.244:4880"
#
# # IP 주소
# ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
# ip = ips.split(' ')[0]
#
# # host name
# user_name = os.getlogin()
# print(user_name)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

@app.route('/usage', methods=['POST'])
def usage():
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    username = json_data['username']
    cpu_usage = json_data['cpu']
    memory_usage = json_data['memory']
    func = json_data['func']

    print(f"User Name : {username} // Function : {func} // CPU Usage : {cpu_usage}% // Memory Usage : {memory_usage}%")

    return "usage"



if __name__ == '__main__':
    app.run(host='192.168.0.14', threaded=True, port='6432')
