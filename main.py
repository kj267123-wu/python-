import requests
import parsel
from lxml import etree
import os
import time

def download_one_chapter(url,headers):
    #爬取一章
    while 1:
        try:
            response = requests.get(url)                              #请求网页，获取网页数据
            break
        except:
            time.sleep(1)
    response.encoding = response.apparent_encoding            #解决乱码问题 万能解码
    #print(response.text)
    #css选择器
    sel = parsel.Selector(response.text)                      #将字符串变成网页

    #########爬取文章标题###############
    h1 = sel.css('h1::text')                                  #css选择器  'h1::text'将对象变为字符串
    title = h1.get()
    if os.path.exists('txt/' +title +'.txt'):
        return 
    print(title)

    #########爬取文章内容
    content = sel.css('#content::text')
    title = h1.get()
    lines = content.getall()
    text = ''
    for line in lines:
        text += line.strip() + '\n'

 #   print(text)

    #print(",".join(content.getall()))
    """保存数据"""
    with open('txt/' +title +'.txt','w',encoding = 'utf-8') as f:
        f.write(title)
        f.write(text)  

#获取所有章节的网址
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Cookie': 'clickbids=10142; Hm_lvt_6dfe3c8f195b43b8e667a2a2e5936122=1599098738; Hm_lpvt_6dfe3c8f195b43b8e667a2a2e5936122=1599098738; Hm_lvt_c979821d0eeb958aa7201d31a6991f34=1599094604,1599096779,1599099334; Hm_lpvt_c979821d0eeb958aa7201d31a6991f34=1599099334',
        } 
while 1:
    try:
        response = requests.get('https://www.biquge.info/10_10142/')
        break
    except:
        time.sleep(1)
response.encoding = response.apparent_encoding             #对网页进行解析，防止网页乱码
a = response.text
#print(response.text)
#解析方法 正则表达式
html = etree.HTML(response.text)
#获取所有请求网址
url_s = html.xpath('//*[@id="list"]/dl/dd') #.getall()变为字符串
for url in url_s:
    url_one = url.xpath('./a/@href')
    print('https://www.biquge.info/10_10142/' +url_one[0])
    download_one_chapter('https://www.biquge.info/10_10142/' +url_one[0],headers)
