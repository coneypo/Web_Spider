# Author:   coneypo
# Created:  08.31
# web spider for xxx.com

from bs4 import BeautifulSoup
import requests
import random
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}


# 设置代理
def get_proxy():
    proxy_url = 'http://www.xicidaili.com/nn/'
    resp = requests.get(proxy_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    ips = soup.find_all('tr')
    proxy_list = []

    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        proxy_list.append(tds[1].text + ':' + tds[2].text)

    proxy = proxy_list[random.randint(0, len(proxy_list))]

    print("Proxy:", proxy)
    return proxy


# 爬取网站
def get_news():
    html = "https://www.ithome.com/blog/"
    resp = requests.get(html, headers=headers, proxies=get_proxy())
    resp.encoding = 'utf-8'

    # 网页内容
    bsObj = BeautifulSoup(resp.content, "lxml")
    #print(bsObj)

    # 分析
    block = bsObj.find_all("div", {"class": "block"})
    #print(block)

    current_titles = []
    current_times = []

    # analysis every block
    for i in range(len(block)):
        # get Time
        time_classes = ["state tody", "state other"]
        for time_class in time_classes:
            tmp = block[i].find_all('span', {'class': time_class})
            if tmp:
                current_time = (block[i].find('span', {'class': time_class})).get_text()
                current_times.append(current_time)

        # get Title
        if block[i].find_all('a', {'target': "_blank"}):
            current_title = (block[i].find('a', {'target': "_blank"})).get_text()
            current_titles.append(current_title)

    for i in range(len(current_times)):
        print(current_times[i], current_titles[i])
    return current_times, current_titles

get_news()

# 计时
start_time = datetime.datetime.now()
tmp = 0
sec_cnt = 0

while 1:
    current_time = datetime.datetime.now()

    # second 是以60为周期
    # 将开始时间的秒second / 当前时间的秒second 进行对比
    if current_time.second >= start_time.second:
        if tmp != current_time.second - start_time.second:
            # print("<no 60>+  ", tmp)
            sec_cnt += 1
            print("Time_cnt:", sec_cnt)
            if sec_cnt % 10 == 0:
                get_news()
                print('\n')
        tmp = current_time.second - start_time.second

    # when get 60
    else:
        if tmp != current_time.second + 60 - start_time.second:
            sec_cnt += 1
            print("Time_cnt:", sec_cnt)

            if sec_cnt % 10 == 0:
                get_news()
                print('\n')
        tmp = current_time.second + 60 - start_time.second