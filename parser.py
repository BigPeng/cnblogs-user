from bs4 import BeautifulSoup
import urllib
import time
from datetime import datetime
def getPage(url):
    try:
        web = urllib.urlopen(url)
        page = web.read()
        web.close()
        return page
    except:
        return None

class Article:
    '''Artible of cnlbogs, contains title,post time,comment num and recommand num...'''
    def __init__(self,title,summary,url,time,rec,view,comment):
        self.title = title
        self.summary = summary
        self.url = url
        self.time = time
        self.rec = rec
        self.view = view
        self.comment=comment
        self.ft = self.str2timef(time)
        self.score = 1.0 * (view/100 +10.0*(rec+0.001)/view  )/(self.ft+5)
    def __cmp__(self,other):
        if self.score > other.score:
            return -1
        elif self.score < other.score:
            return -1
        else:
            return 0
    def __str__(self):
        s =  self.title.encode('gbk')
        s += '\n\t'+self.url.encode('gbk')
        s += '\n\t'+self.time.encode('gbk')
        s += '\tRead('+ str(self.view)+')'+')\tRecommend('+str(self.rec)+')'
        s += '\tScore('+str(self.score)+')'
        return s
    def str2timef(self,str_t):
        format = '%Y-%m-%d %H:%M'
        #str_t = str_t.encode('utf-8')
        dt = datetime.strptime(str_t,format)
        t =  time.mktime(dt.timetuple()) 
        #return t 
        ct = time.time()
        return (ct - t) / 600

def getOnePageArticles(page_soup):
    articles = []
    post_list = page_soup.find(id='post_list')
    for content in post_list.contents:
        if len(content) < 2:
            continue
        rec = int(content.find('span',{'class':'diggnum'}).get_text())
        titlelnk = content.find('a',{'class':'titlelnk'})
        title = titlelnk.get_text()
        url = titlelnk.get('href')
        summary = content.find('p',{'class':'post_item_summary'}).get_text()
        post = content.find('div',{'class':'post_item_foot'}).contents[2]
        post_t = post.strip()[4:]
        comment = content.find('span',{'class':'article_comment'}).get_text()
        com_num =comment[comment.find('(')+1:-1]
        view = content.find('span',{'class':'article_view'}).get_text()
        view_num =int(view[view.find('(')+1:-1])
        article = Article(title,summary,url,post_t,rec,view_num,com_num)
        articles.append(article)
    return articles

def getArticles(p):
    articles = []
    home = 'http://www.cnblogs.com/sitehome/p/'
    for i in xrange(p):
        url = home+str(i+1)
        print url
        page = getPage(url)
        soup = BeautifulSoup(page)
        articles += getOnePageArticles(soup)
    return articles


articles = getArticles(5)
articles.sort(key=lambda x:x.score,reverse=True)
count  = 1
print 'Update at ',time.ctime()
for each in articles:
    if count % 25 == 1:
        print 'Page',1 + count/25
    print count, '\t', each
    count += 1
