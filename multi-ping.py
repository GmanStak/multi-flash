from prometheus_client import Gauge, generate_latest
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from multiping import MultiPing
import argparse

import logging
app = Flask(__name__)

#添加配置文件路径
#app.config.from_pyfile('../config/config.cfg')

#控制台不输出“GET”日志
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#获取设备列表
def getFile():
    iplist = []
    with open('../listfile/ipList', 'r') as f:
        for line in f.readlines():
            iplist.append(line.rsplit('\n')[0])
        f.close()
    return iplist

@app.route('/')
def index():
    return "Hello World"

@app.route("/metrics")
def ping_status():
    iplist = getFile()
    mp = MultiPing(iplist)
    mp.send()
    responses, no_responses = mp.receive(0.1)
    registry = CollectorRegistry()
    ping_status = Gauge('ping_status', 'This is a ping-status metrics', ['job', 'action', 'port', 'instance', 'target'],
                  registry=registry)
    #遍历成功的字典：{“设备ip”：“ping时间”}
    for ip in responses:
        ping_status.labels(job=ip, action='ping', port='000', instance=ip, target=ip).inc(1)
    #遍历失败的列表：["设备ip1","设备ip2"]
    for ip in no_responses:
        ping_status.labels(job=ip, action='ping', port='000', instance=ip, target=ip).inc(0)
    return Response(generate_latest(registry), mimetype="text/plain")

if __name__ == "__main__":
    #创建参数
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--ipaddress", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=str, default="5000")
    args = parser.parse_args()
    ipaddress = args.ipaddress
    port = args.port
    app.run(host=ipaddress, port=port)