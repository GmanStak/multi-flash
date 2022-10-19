# multi-flash
# python版本3.10
# 基于python-flask框架实现Prometheus采集对应设备IP的ping状态，相当于blackbox_exporter功能
# 使用的ping工具：multiping
# 目录结构
# mping
#--|->bin
#----|->multi-ping.py
#--|->config
#----|->config.cfg
#--|->listfile
#----|->ipList
# 可用外部参数：--ipaddress， --port
# 地址访问：http://localhost:5000/metrics
