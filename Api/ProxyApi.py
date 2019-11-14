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
    # '/delete?proxy=host:port': u'删除一个代理IP',
    '/get': u'获取一个代理IP',
    # '/get_all': u'获取所有代理IP',
    '/get_status': u'代理池当前状态',
    # '/refresh': u'刷新代理池(refresh会有守护程序定时执行，由api直接调用性能较差，不建议使用)',
    '/user_agent': '获取一个USER_AGENT',
    '使用方法': 'host:port/关键词'
}


@app.route('/')
def index():
    return api_list


# @app.route('/delete/', methods=['GET'])
# def delete():
#     proxy = request.args.get('proxy')
#     ProxyManager().delete(proxy)
#     return 'success'


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'


# @app.route('/get_all/')
# def getAll():
#     proxies = ProxyManager().getAll()
#     return proxies


@app.route('/get_status/')
def getStatus():
    status = ProxyManager().getNumber()
    return status


# @app.route('/refresh/')
# def refresh():
#     # TODO refresh会有守护程序定时执行，由api直接调用性能较差，不建议使用
#     ProxyManager().refresh()
#     return 'success'


@app.route('/user_agent/')
def user_agent():
    user_agent_list = [
        # Android
        # 小米手机
        'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn;  MI2 Build/JRO03L) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 XiaoMi/MiuiBrowser/1.0',
        # 魅族手机
        'JUC (Linux; U; 2.3.5; zh-cn; MEIZU MX; 640*960) UCWEB8.5.1.179/145/33232',
        # Nexus 7(Tablet)
        'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
        # Samsung Galaxy S3(Handset)
        'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        # Samsung Galaxy Tab(Tablet)
        'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',

        # 国产浏览器
        # 360安全浏览器
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        # 360极速浏览器
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360Chrome)',
        # 猎豹浏览器
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36 LBBROWSER',
        # UC浏览器电脑版
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 UBrowser/5.1.2238.18 Safari/537.36',
        # UC浏览器手机版
        'UCWEB/2.0 (iOS; U; iPh OS 4_3_2; zh-CN; iPh4) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
        # 搜狗浏览器
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
        # 百度浏览器
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 BIDUBrowser/7.5 Safari/537.36',
        # 遨游浏览器
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        # QQ浏览器
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36 QQBrowser/9.0.2229.400',
        # QQ浏览器手机版
        'MQQBrowser/3.6/Adr (Linux; U; 4.0.3; zh-cn; HUAWEI U8818 Build/U8818V100R001C17B926;480*800)',
        # 微信内置浏览器
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 MicroMessenger/5.0.1',

        # Google Chrome
        # Chrome on Android Mobile
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
        # Chrome on Android Tablet
        'Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
        # Chrome on Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        # Chrome on Ubuntu
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36',
        # Chrome on Windows
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        # Chrome on iPhone
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25',

        # Internet Explorer
        # Internet Explorer 6
        'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)',
        # Internet Explorer 7
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        # Internet Explorer 8
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        # Internet Explorer 9
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        # Internet Explorer 10
        'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',

        # Firefox
        # Firefox on Android Mobile
        'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
        # Firefox on Android Tablet
        'Mozilla/5.0 (Android; Tablet; rv:14.0) Gecko/14.0 Firefox/14.0',
        # Firefox on Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
        # Firefox on Ubuntu
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
        # Firefox on Windows
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',

        # Opera
        # Opera on Mac
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
        # Opera on Windows
        'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',

        # Safari
        # Safari on Mac
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        # Safari on Windows
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        # Safari on iPad
        'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        # Safari on iPhone
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',

        # Windows Phone
        # Windows Phone 7
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; LG; GW910)',
        # Windows Phone 7.5
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; SAMSUNG; SGH-i917)',
        # Windows Phone 8
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)',

        # iOS
        # iPad
        'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        # iPhone
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        # iPod
        'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3',

        # 其他
        # BlackBerry - Playbook 2.1
        'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML, like Gecko) Version/7.2.1.0 Safari/536.2+',
        # MeeGo - Nokia N9
        'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13',

    ]
    user_agent_one = random.sample(user_agent_list, 1)[0]
    return user_agent_one


def run():
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
