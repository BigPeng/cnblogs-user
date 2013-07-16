# -*- coding: utf-8 -*-
from myproperty import DOMAIN
import urllib
import os
import re
import html2text


baseDir = "posts"
classLable = {"doNet技术":"108698","编程语言":"2","软件设计":"108701",
              "web前端":"108703","企业信息化":"108704","手机开发":"108705",
              "数据库技术":"108712","操作系统":"108724","其它分类":"4"
              }
##classLable = {"B":"2",
##              "D":"108703","E":"108704","F":"108705",
##              "G":"108712","H":"108724","I":"4"
##              }
postUrlReg = '''<div class="post_item_body">\s+<h3><a class="titlelnk" href="(http://www.cnblogs.com/.*html)" target="_blank">(.+)</a>'''
postUrlMatcher = re.compile(postUrlReg)

nextPageReg = '''<a href="(/cate/\d+/\d+)" onclick="aggSite.loadCategoryPostList\(\d+,\d+\);buildPaging\(\d+\);return false;">Next '''
nextPageUrlMatcher = re.compile(nextPageReg)

def getPage(url):
    try:
        web = urllib.urlopen(url)
        page = web.read()
        web.close()
        return page
    except:
        return None
def getText(html,encoding):
    h = html2text.HTML2Text(baseurl="")
    h.ignore_links = True
    data = html.decode(encoding)
    return h.handle(data)

def formatTitle(title,encoding):    
    while ' ' in title:
        title = title.replace(' ',"")
    while ':' in title:
        title = title.replace(':',"")
    while '：' in title:
        title = title.replace('：',"")
    while '“' in title:
        title = title.replace('“',"")
    while '”' in title:
        title = title.replace('”',"")                 
    while '"' in title:
        title = title.replace('"',"")
    while '/' in title:
        title = title.replace('/',"")
    while '?' in title:
        title = title.replace('?',"")
    while '？' in title:
        title = title.replace('？',"")
    while '\\' in title:
        title = title.replace('\\',"")
    while '*' in title:
        title = title.replace('*',"")
    while '|' in title:
        title = title.replace('|',"")
    title = title.decode(encoding)
    return title
    
def crawPagePost(className,path,page):
    encoding = 'utf-8'
    posts = postUrlMatcher.findall(page)
    for postUrl,title in posts:
        html = getPage(postUrl)
        if html == None:
            continue
        text = getText(html,encoding)
        text = text.encode(encoding)
        title = formatTitle(title,encoding)
        print title
        textFile = open(os.path.join(path,title),'w')
        textFile.write(text)
        textFile.flush()
        textFile.close()

def getNextPageUrl(page):
    nextUrl =nextPageUrlMatcher.findall(page)
    if len(nextUrl) > 0:
        return DOMAIN+nextUrl[0]
    return None
        
def crawPost(className,url):
    className = className.decode('utf-8')
    path = os.path.join(baseDir,className)
    if os.path.isdir(path) == False:
        os.makedirs(path)
    page = getPage(url)
    if page == None:
        return
    crawPagePost(className,path,page)
    nextPageUrl = getNextPageUrl(page)
    while nextPageUrl != None:
        print nextPageUrl
        page = getPage(nextPageUrl)
        if page == None:
            break
        crawPagePost(className,path,page)
        nextPageUrl = getNextPageUrl(page)

def craw():
    if os.path.isdir(baseDir) == False:
        os.makedirs(baseDir)
    for className,suffix in classLable.items():
        url = DOMAIN+"/cate/"+suffix
        crawPost(className,url)
if __name__=="__main__":
    craw()

