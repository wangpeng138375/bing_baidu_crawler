# encoding=utf-8
'''
Created on 2018-03-19
'''
import bs4
from bs4 import BeautifulSoup as bs
import urllib2 as url
import urllib
import re,traceback
import Queue

class BaiduSpider(object):
    '''
    根据url爬取数据
    '''
    def __init__(self,url):

        self._start_url = url

    def _get_html(self):
        res = url.urlopen(self._start_url,timeout=10)
        result=res.read().decode("utf-8")
        print result
        return result

    def _get_content(self,content):
        # 先要把bs4.element.NavigableString类型转化为string类型
        return reduce(lambda x,y:x+y,map(lambda x:x.replace("<em>","").replace("</em>",""),
                                     map(lambda x:x.string,content)))
    def get_titles_contents(self):
        result_title_contents=[]
        soup = bs(self._get_html(),"lxml")
        # 找到左边内容到的跟节点
        base_div = soup.select("#content_left")[0] # base_div_list是一个列表
        
        
        childs = base_div.children
        for child in childs:
            # isinstance(child,bs4.element.Tag) 用来过滤掉\n
            # 'c-container' in child['class'] 用来过滤掉广告
            # child.div 过滤掉其他的干扰
            if isinstance(child,bs4.element.Tag) and child.div and child.get('class',None) and 'c-container' in child['class']:
                # 获取到title所在的tag
                # title所在的class标签为class=t
                title = child.select(".t")[0]
        
                #print "链接:",title.a["href"]
                
                #print "标题",self._get_content(title.a.contents)
                result_title_contents.append(self._get_content(title.a.contents))
                # 查找abstract所在的tag
                # abstract坐在的class标签是class=c-abstract
                abstract = child.select(".c-abstract")
                # 如果没有找到c-abstract标签，则试着找下.c-span18标签
                if 0 == len(abstract):
                    abstract = child.select(".c-span18")
        
                #
                if 0 != len(abstract):
                    abstract_str = ""
                    
                    for c in abstract[0].children:
                        if isinstance(c,bs4.element.NavigableString):
                            if c.string!="\n":

                                c.string=re.sub("[\s\.\!\/\?_,$%^*+\"\'——()?【】“”！，。？、~@#￥%……&*（）]+", "",c.string)
                                abstract_str += c.string
                        if isinstance(c,bs4.element.Tag):
                            for c1 in c.children:
                                if isinstance(c1,bs4.element.NavigableString):
                                    if c1.string!="\n":
                                        c1.string=re.sub("[\s\.\!\/\?_,$%^*+\"\'——()?【】“”！，。？、~@#￥%……&*（）]+", "",c1.string)
                                        abstract_str += c1.string
                    #print "概要:",abstract_str
                    result_title_contents.append(abstract_str)
        return result_title_contents
   



if '__main__' == __name__:
    
    
    FILE_OUTPUT = "baidu_output.txt"
    outfd=open(FILE_OUTPUT,"w")
    fd=open("input.csv","r")
    q = Queue.Queue() #创建队列对象
    for l in fd:
        llist=l.strip().split("\t")[0:2]
        for ll in llist:
            url_page1="http://www.baidu.com/s?rn=50&tn=95752409_hao_pg&ssl_sample=hao_1&" + urllib.urlencode({"wd": ll})
            url_page2="http://www.baidu.com/s?rn=50&tn=95752409_hao_pg&ssl_sample=hao_1&pn=50&" + urllib.urlencode({"wd": ll})
            url_page3="http://www.baidu.com/s?rn=50&tn=95752409_hao_pg&ssl_sample=hao_1&pn=100&" + urllib.urlencode({"wd": ll})
            q.put(url_page1)
            q.put(url_page2)
            q.put(url_page3)
    while not q.empty():
        one = q.get()
        try:
            print one
            one_crawler=BaiduSpider(one)
            for utterance in one_crawler.get_titles_contents():
                print utterance
                outfd.write(utterance.encode("utf8"))
                
                outfd.write("\n")
        except Exception,e:
            print "error"
            traceback.print_exc()
            q.put(one)
    outfd.close()
