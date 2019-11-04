import sys
import random
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
    '/delete?proxy=host:port': u'删除一个代理IP',
    '/get': u'获取一个代理IP',
    '/get_all': u'获取所有代理IP',
    '/get_status': u'代理池当前状态',
    '/refresh': u'刷新代理池(refresh会有守护程序定时执行，由api直接调用性能较差，不建议使用)',
    '/user_agent': '获取一个USER_AGENT',
    '使用方法': 'host:port/关键词'
}


@app.route('/')
def index():
    return api_list


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'


@app.route('/get_all/')
def getAll():
    proxies = ProxyManager().getAll()
    return proxies


@app.route('/get_status/')
def getStatus():
    status = ProxyManager().getNumber()
    return status


@app.route('/refresh/')
def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，不建议使用
    ProxyManager().refresh()
    return 'success'


@app.route('/user_agent/')
def user_agent():
    user_agent_list = [
        # IE
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        # Firefox
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    ]
    user_agent_one = random.sample(user_agent_list, 1)[0]
    return user_agent_one


def run():
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
