import sys
from werkzeug.wrappers import Response
from flask import Flask, jsonify, request

sys.path.append('../')

from Config.ConfigGetter import config
from Manager.ProxyManager import ProxyManager

app = Flask(__name__)


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse

api_list = {
    'delete?proxy=host:port': u'删除一个代理IP',
    'get': u'获取一个代理IP',
    'get_all': u'获取所有代理IP',
    'get_status': u'代理池当前状态',
    'refresh': u'刷新代理池(refresh会有守护程序定时执行，由api直接调用性能较差，不建议使用)',
    '使用方法': 'host:port/关键词'
}


@app.route('/')
def index():
    return api_list


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'


@app.route('/refresh/')
def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，不建议使用
    ProxyManager().refresh()
    return 'success'


@app.route('/get_all/')
def getAll():
    proxies = ProxyManager().getAll()
    return proxies


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@app.route('/get_status/')
def getStatus():
    status = ProxyManager().getNumber()
    return status


def run():
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
