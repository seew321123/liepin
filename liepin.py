from pyquery import PyQuery as pq
import requests
from urllib import parse
from xlwt import Workbook
import sys
import requests.adapters

requests.adapters.DEFAULT_RETRIES =5       # 增加重连次数
s = requests.session()
s.keep_alive = False# 关闭多余连接

#以下是代理信息配置--------------------------------------------------------------------------------------------------------------------------
proxy_host = 'tps172.kdlapi.com'
proxy_port = '15818'
proxy_user = 't18095048596964'
proxy_pass = '9oxhhjcd'
proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' %{
    'host':proxy_host,
    'port':proxy_port,
    'user':proxy_user,
    'pass':proxy_pass,
}
proxies = {
    'http':proxy_meta,
    'https':proxy_meta,
}
#以上内容是代理信息的配置----------------------------------------------------------------------------------------------------------------------


sys.setrecursionlimit(1000000)
row_num = 0
data = []
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Encoding': 'Gzip'
}
r = s.get('https://www.liepin.com/zhaopin/?isAnalysis=&dqs=020&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=爬虫&init=-1&searchType=1&headckid=351c3e85f3b78009&compkind=&fromSearchBtn=2&sortFlag=15&ckid=7cb72f717d699b09&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=_dBUvSI8zq_TVVe6zv63rg~r3i1HcfrfE3VRWBaGW6LoA&d_sfrom=search_prime&d_ckId=dad3f8e5c6a462737b639494ae6bb101&d_curPage=8&d_pageSize=40&d_headId=3ef0ee3cf36bd0058b86c5333eb80bf7&curPage=0',headers = headers,proxies = proxies)
text = r.text
#print(text)             #测试输出

def findJob(txt):
    #将原先的text作为函数的参数txt传入
    html = pq(txt)           #参数txt也就是之前的text
    jobPageUrl = html('#sojob ul.sojob-list li .sojob-item-main .job-info h3 a').items()
    for item in jobPageUrl:
            url = parse.urljoin('https://www.liepin.com',item.attr('href'))
            #print(url)          #测试输出
            #以上代码获取到了第一页检索结果中的所有职位的单独页面url
            #接下来需要以这些url为起点再次一个一个发起请求并检索页面内的信息
            r_2 = s.get(url,headers = headers,proxies = proxies)
            text_2 = r_2.text
            html2 = pq(text_2)
            job_name = html2('h5').text()
            job_detail = html2('.content.content-word').text()
            data_item = [job_name,job_detail,url]
            data.append(data_item)
            print(len(data))           #输出data的长度，用来在线监测是否继续运行
            print(url)
            if len(data) == 300:
                return
    next_page = html('a:contains("下一页")')
    next_url_half = next_page.attr('href')
    next_url = parse.urljoin('https://www.liepin.com',next_url_half)
    r_3 = s.get(next_url,headers = headers,proxies = proxies)
    text_3 = r_3.text
    #将text_3作为参数传入到函数findJob中，发起循环
    findJob(text_3)


findJob(text)
#以下操作用于保存数据至excel文件当中-------------------------------------------------------------------------------------------------------------
book = Workbook()
sheet1 = book.add_sheet('list')
for item in data:
    sheet1.write(row_num,0,label = item[0])
    sheet1.write(row_num,1,label = item[1])
    sheet1.write(row_num,2,label = item[2])
    row_num += 1
    book.save('job_pachong.xls')


