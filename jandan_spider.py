import requests
from lxml import etree
import base64
headers = {'referer': 'http://jandan.net/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}

# 保存图片
def save_jpg(req_url,i):
    index=1
    html = requests.get(req_url, headers=headers,timeout=1).text  #class=str
    html = etree.HTML(html)#调用HTML类进行初始hua,构造了XPath解析对象,etree模块可以自动修正HTML文本。

    # 抓取图片链接
    for link in html.xpath('//div[@class="text"]/p/span[@class="img-hash"]/text()'):
        # 构造完整url 2018/8/13 煎蛋网图片链接被base64加密
        link = 'https:' + str(base64.b64decode(link),'utf-8')
        # 打印日志
        print('当前抓取链接:',req_url,'-----',link)
        # 保存命名格式为 页数.张数.jpg
        with open('F:/from_jiandan_png/'+'page{0}.{1}.{2}'.format(i,index,format(link[-4:])), 'wb') as jpg:
            try:
                # 获取图片，如果请求异常，由raise_for_status() 抛出异常进入except
                r = requests.get(link,timeout=1)
                r.raise_for_status()
                jpg.write(r.content)
                # 打印日志
                print("正在抓取第%s条数据" % index,'文件保存为：page{0}.{1}.{2}'.format(i,index,format(link[-4:])))
            except:
                continue
        index+=1

#  抓取煎蛋妹子图片
if __name__ == '__main__':
    for i in range(1, 47):
        # url中str（i）表示第几页
        url = "http://jandan.net/ooxx/page-" + str(i) + "#comments"
        save_jpg(url, i)
