##### proxy_pool 爬虫可维护代理池


* 借鉴于：https://github.com/jhao104/proxy_pool
* 2019.06.06 新增11个免费代理源


### 一、下载安装
```shell
git clone https://github.com/guoxianru/proxy_pool
```

### 二、安装依赖
```shell
pip install -r requirements.txt
```

### 三、配置Config/setting.py
* Config/setting.py 为项目配置文件
```shell
1.配置数据库
DATABASES = {
    "default": {
        "TYPE": "SSDB",             # 如果使用SSDB或redis数据库，均配置为SSDB
        "HOST": "39.106.189.108",   # db host(生成环境请配置为公网IP)
        "PORT": 6379,               # db port
        "NAME": "proxy",            # 数据库名称
        "PASSWORD": ""              # 数据库密码
    }
}

2.配置 ProxyGetter
PROXY_GETTER = [
    "freeProxyFirst",      # 启用的代理抓取函数名，在 ProxyGetter/getFreeProxy.py 扩展
    ....
]

3.配置 API 服务
SERVER_API = {
    "HOST": "0.0.0.0",  # 监听ip, 0.0.0.0 监听所有IP
    "PORT": 5010        # 监听端口
}

4.上面配置启动后，代理池访问地址为 39.106.189.108:5010
```

### 四、启动
```shell
# 如果你的依赖已经安全完成并且具备运行条件,可以直接在Run下运行main.py
# 到Run目录下:  python main.py
# 如果运行成功你应该看到有4个main.py进程
# 你也可以分别运行他们,依次到Api下启动ProxyApi.py,Schedule下启动ProxyRefreshSchedule.py和ProxyValidSchedule.py即可.
```

### 五、Docker

1.开发环境 Docker
```shell
# Workdir proxy_pool
docker build -t proxy_pool .
docker run -it --rm -v $(pwd):/usr/src/app -p 5010:5010 proxy_pool
```
2.生产环境 Docker/docker-compose
```shell
# Workdir proxy_pool
docker build -t proxy_pool .
pip install docker-compose
docker-compose -f docker-compose.yml up -d --build
```

### 六、使用

1.可以通过api访问 39.106.189.108:5010 查看
```shell
/get	        GET	随机获取一个代理	None
/get_all	    GET	获取所有代理	None
/get_status	    GET	查看代理数量	None
/delete	GET	    删除代理	proxy=host:ip
```

2.爬虫使用
* 如果要在爬虫代码中使用的话， 可以将此api封装成函数直接使用，例如：
```python
import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

#your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get('https://www.example.com', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None
```

### 七、扩展代理
* 添加一个新的代理获取方法如下:

1.首先在GetFreeProxy类中添加你的获取代理的静态方法， 该方法需要以生成器(yield)形式返回host:ip格式的代理，例如:
```python
class GetFreeProxy(object):
    # 你自己的方法
    @staticmethod
    def freeProxyCustom():  # 命名不和已有重复即可
        # 通过某网站或者某接口或某数据库获取代理 任意你喜欢的姿势都行
        # 假设你拿到了一个代理列表
        proxies = ["139.129.166.68:3128", "139.129.166.61:3128", ...]
        for proxy in proxies:
            yield proxy
        # 确保每个proxy都是 host:ip正确的格式就行
```

2.添加好方法后，修改Config/setting.py文件中的PROXY_GETTER项：
* 在PROXY_GETTER下添加自定义的方法的名字:
```python
PROXY_GETTER = [
    "freeProxyFirst",
    ...
    "freeProxyCustom"  #  # 确保名字和你添加方法名字一致
]
```
* ProxyRefreshSchedule会每隔一段时间抓取一次代理，下次抓取时会自动识别调用你定义的方法。