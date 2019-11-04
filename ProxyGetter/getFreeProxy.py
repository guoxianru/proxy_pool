import re
import sys
import requests

sys.path.append('..')

from lxml import etree
from Util.WebRequest import WebRequest
from Util.utilFunction import getHtmlTree

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):
    """
    proxy getter
    """

    @staticmethod
    def payProxy_wuyou():
        """
            无忧代理
            http://www.data5u.com/
        """
        try:
            order = 'c714e62db21d6bfb4867ae6598ff35bb'
            apiUrl = 'http://api.ip.data5u.com/dynamic/get.html?order=' + order
            res = requests.get(apiUrl).content.decode()
            ips = res.split('\n')
            for ip in ips:
                yield ip
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_iphai():
        """
            IP海
            http://www.iphai.com/free
        """
        try:
            urls = [
                'http://www.iphai.com/free/ng',
                'http://www.iphai.com/free/np',
                'http://www.iphai.com/free/wg',
                'http://www.iphai.com/free/wp'
            ]
            request = WebRequest()
            for url in urls:
                r = request.get(url, timeout=10)
                re_str = r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>'
                proxies = re.findall(re_str, r.text)
                for proxy in proxies:
                    yield ":".join(proxy)
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_89(count=3000):
        """
            89代理
            http://www.89ip.cn/index.html
            count: 提取数量
        """
        try:
            response = requests.get(url='http://www.89ip.cn/tqdl.html?api=1&num=' + str(count) + '&port=&address=&isp=')
            data = re.findall("\n</script>(.*?)高", response.text, re.S)[0]
            ip_list = data.replace('\n', '').split('<br>')[:-1]
            for ip in ip_list:
                yield ip
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_kuai(page_count=5):
        """
            快代理
            https://www.kuaidaili.com/free/
            page_count: 提取页数
        """
        try:
            url_list = [
                'https://www.kuaidaili.com/free/inha/',
                'https://www.kuaidaili.com/free/intr/'
            ]
            for u in url_list:
                for i in range(1, page_count + 1):
                    url = u + str(i)
                    tree = getHtmlTree(url)
                    proxy_list = tree.xpath('.//table//tr')
                    for tr in proxy_list[1:]:
                        yield ':'.join(tr.xpath('./td/text()')[0:2])
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_yun(page_count=5):
        """
            云代理
            http://www.ip3366.net/free/
            page_count: 提取页数
        """
        try:
            url_list = [
                'http://www.ip3366.net/free/?stype=1&page=',
                'http://www.ip3366.net/free/?stype=2&page='
            ]
            request = WebRequest()
            for u in url_list:
                for i in range(1, page_count + 1):
                    url = u + str(i)
                    r = request.get(url, timeout=10)
                    proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
                    for proxy in proxies:
                        yield ":".join(proxy)
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_xici(page_count=1):
        """
            西刺代理
            https://www.xicidaili.com/
            page_count: 提取页数
        """
        url_list = [
            'http://www.xicidaili.com/nn/',
            'http://www.xicidaili.com/nt/',
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxy_xila(page_count=4):
        """
            西拉代理
            http://www.xiladaili.com/
            page_count: 提取页数
        """
        for page in range(1, page_count + 1):
            url = 'http://www.xiladaili.com/gaoni/' + str(page)
            html_tree = getHtmlTree(url)
            ip_list = html_tree.xpath("//table[@class='fl-table']//tr")[1:]
            for i in ip_list:
                ip = i.xpath("./td[1]/text()")[0]
                score = i.xpath("./td[8]/text()")[0]
                try:
                    yield ip
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxy_qiyun(page_count=10):
        """
            旗云代理
            http://www.qydaili.com/free/
            page_count: 提取页数
        """
        try:
            request = WebRequest()
            for page in range(1, page_count + 1):
                url = 'http://www.qydaili.com/free/?action=china&page=' + str(page)
                r = request.get(url, timeout=10)
                proxies = re.findall(r'<td data-title="IP">(.*?)</td>[\s\S]*?<td data-title="PORT">(\d+)</td>', r.text)
                for proxy in proxies:
                    yield ":".join(proxy)
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_nima(page_count=1):
        """
            泥马代理
            http://www.nimadaili.com/
            page_count: 提取页数
        """
        url_list = [
            'http://www.nimadaili.com/putong/',
            'http://www.nimadaili.com/gaoni/',
            'http://www.nimadaili.com/http/',
            'http://www.nimadaili.com/https/'
        ]
        try:
            request = WebRequest()
            for u in url_list:
                for i in range(1, page_count + 1):
                    url = u + str(i)
                    r = request.get(url, timeout=10)
                    proxies = re.findall(r'<td>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5})</td>', r.text)
                    for proxy in proxies:
                        yield proxy
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_shenji():
        """
            神鸡代理
            http://www.shenjidaili.com/open/
        """
        try:
            url = 'http://www.shenjidaili.com/open/'
            request = WebRequest()
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5})</td>', r.text)
            for proxy in proxies:
                yield proxy
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy_xiaoshu():
        """
            小舒代理
            http://www.xsdaili.com/
        """
        shouye = requests.get(url='http://www.xsdaili.com/')
        shouye.encoding = shouye.status_code
        html_shouye = etree.HTML(shouye.text)
        new_url = html_shouye.xpath("//div[@class='col-md-12'][2]/div/div[@class='title']/a/@href")[:2]
        for url in new_url:
            url = 'http://www.xsdaili.com' + url
            ip_ye = requests.get(url)
            ip_ye.encoding = ip_ye.status_code
            html_ip = etree.HTML(ip_ye.text)
            data = html_ip.xpath("string(//div[@class='cont'])")
            ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,3}', data)
            try:
                for ip in ips:
                    yield ip
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxy_proxylistplus(page_count=4):
        """
            ProxyListplus
            https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
            page_count: 提取页数
        """
        try:
            for i in range(1, page_count + 1):
                url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'.format(i)
                request = WebRequest()
                r = request.get(url, timeout=10)
                proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
                for proxy in proxies:
                    yield ':'.join(proxy)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    from CheckProxy import CheckProxy

    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_iphai)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_89)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_kuai)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_yun)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_xici)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_xila)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_qiyun)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_nima)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_shenji)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_xiaoshu)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy_proxylistplus)

    # CheckProxy.checkAllGetProxyFunc()
