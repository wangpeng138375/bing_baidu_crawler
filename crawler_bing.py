# encoding=utf-8
'''
Created on 2018-03-13
'''
import urllib, re, urllib2, traceback, time

from bs4 import BeautifulSoup
import Queue

def crawlerToStr(url, data=None):
    data = {"q": data, "pq": data, "qs": "n", "sp": "-1", "FORM": "PERE", "first": "0", "count": "100"}
    datau = urllib.urlencode(data)

    req = urllib2.Request(url + datau)
    print req._Request__original
    req.add_header('Referer', 'http://www.baidu.com')
    req.add_header('Content-Language', 'zh')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    r = urllib2.urlopen(req, timeout=10)
    html = r.read()

    return html


def searchWithBing(key):
    result=[]
    bing_search = 'https://www.bing.com/search?'

    html = crawlerToStr(bing_search, key)
    # print html

    soup = BeautifulSoup(html, "html.parser")
    content = soup.find('ol', {"id": "b_results"})
    index = 0
    for i in content.findAll("li", {"class": "b_ad"}):
        index += 1

        title1 = i.find("h2").get_text()
        result.append(title1.encode("utf8"))
        content1 = i.find("p").get_text()
        result.append(content1.encode("utf8"))

    for i in content.findAll("div", {"class": "b_overflow"}):
        index += 1
        # print "=========================================="
        text1 = i.get_text()
        result.append(text1.encode("utf8"))
        # print index," 2 -----------------------------------------"

        # print "=========================================="
    for i in content.findAll("li", {"class": "b_algo"}):
        index += 1
        # print "=========================================="
        title2 = i.find("h2").get_text()
        result.append(title2.encode("utf8"))

        # print index," 3 -----------------------------------------"
        pp = i.find("p")
        if pp:
            content2 = pp.get_text()

            result.append(content2.encode("utf8"))
    return result
if __name__ == '__main__':

    FILE_OUTPUT = "bing_output.txt"
    outfd=open(FILE_OUTPUT,"w")
    fd=open("input.csv","r")
    allline=[]
    q = Queue.Queue() #创建队列对象
    for l in fd:
        llist=l.strip().split("\t")[0:2]
        for ll in llist:
            allline.append(ll)
    #使用队列的方式
    for line in allline:
        q.put(line)    #在队列尾部插入元素
    while not q.empty():
        one = q.get()
        try:
            one_crawler=searchWithBing(one)
            for utterance in one_crawler:
                outfd.write(utterance)
                outfd.write("\n")
        except Exception,e:
            print "error"
            traceback.print_exc()
            q.put(one)
    outfd.close()




