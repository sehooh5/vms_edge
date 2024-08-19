#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# /res_edge_data(POST 추가)

# - 기존 POST 방식에서 변경
# - 매초 전달되는 json 파일 저장하기
@app.route('/save_edgeData', methods=['POST'])
def save_edgeData():
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    code = json_data['code']
    message = json_data['message']
    nid = json_data['nid']
    created_at = json_data['created_at']
    res_class = json_data['res_class']
    res_confidence = json_data['created_at']

    print(f"code : {code} // message : {message} // nid : {nid} // time : {created_at} // res_class : {res_class} // res_confidence : {res_confidence}")

    # db에 저장하는 기능


    return response.message('0000')


# TEST SW 데이터 전송받는 API
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
