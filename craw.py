# -*- coding: utf-8 -*-


from myproperty import DOMAIN,USER_HOME
import urllib
import re
import urllib2
import time

def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read()
    page.close()
    return html

def getOnePageFriends(html):
    reg = '''<div class="avatar_name">\r\n                <a href="/u/([A-Za-z0-9_-]*)/"'''
    friends = re.compile(reg).findall(html)
    return friends

def getNextPageUrl(html,userId,tag):
    nextReg = '''<a href="(/u/'''+userId+tag+'''\d*/)">Next'''
    nextPage = re.compile(nextReg).findall(html)
    if len(nextPage)==0:
        return None
    return USER_HOME +nextPage[0] 
    
def getFollowees(userId):
    tag= "/followees/"
    url = USER_HOME + "/u/" +userId+tag
    html = getHtml(url)
    followees = getOnePageFriends(html)
    nextUrl = getNextPageUrl(html,userId,tag)
    while nextUrl != None:
        html = getHtml(nextUrl)
        followees += getOnePageFriends(html)
        nextUrl = getNextPageUrl(html,userId,tag) 
    return followees

    
def getFollowers(userId):
    tag = "/followers/"
    url = USER_HOME + "/u/" +userId+tag
    html = getHtml(url)
    followers = getOnePageFriends(html)
    nextUrl = getNextPageUrl(html,userId,tag)
    while nextUrl != None:
        html = getHtml(nextUrl)
        followers += getOnePageFriends(html)
        nextUrl = getNextPageUrl(html,userId,tag)
    return followers

def getNick(html):
    reg = '''Copyright &copy;[2013]* (\S*)'''
    name = re.compile(reg).findall(html)
    if len(name) == 0:
        return 'NoneNick'
    return name[0]

def getPostAndCommentNum(html):
    reg = '''Posts\s*-\s*([\d]*)&nbsp;\s*Articles\s*-\s*[\d]*&nbsp;\s*Comments\s*-\s*([\d]*)&nbsp;'''
    nums = re.compile(reg).findall(html)
    if len(nums) != 0:
        return nums[0]
    reg = '''随笔\s*-\s*([\d]*)&nbsp;\s*文章\s*-\s*[\d]*&nbsp;\s*评论\s*-\s*([\d]*)&nbsp;'''
    nums = re.compile(reg).findall(html)
    if len(nums) != 0:
        return nums[0]
    reg = '''随笔\s*-\s*([\d]*)&nbsp;\s*评论\s*-\s*([\d]*)&nbsp;\s*文章\s*-\s*[\d]*&nbsp;'''
    nums = re.compile(reg).findall(html)
    if len(nums) != 0:
        return nums[0]
    reg = '''<h3>统计</h3>\s*<ul>\s*<li>\s*随笔\s*-\s*([\d]+)\s*<li>\s*文章\s*-\s*\d+\s*<li>\s*评论\s*-\s*([\d]+)'''
    nums = re.compile(reg).findall(html)
    if len(nums) != 0:
        return nums[0]
def getCountByScan(html,nick):
    reg = '''posted\s*@\s*\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}\s+'''+nick+'''\s+阅读\(\d+\)\s+评论\((\d+)\)\s*<a href'''
    commentNums = re.compile(reg).findall(html)
    postCount = len(commentNums)
    commentCount = 0
    if postCount != 0:
        for each in commentNums:
            commentCount += int(each)
    return postCount,commentCount
            
def getNextHomePageUrl(html,userId):
    reg = '''<a href="(http://www.cnblogs.com/'''+userId+'''/default.html\?page=\d+&amp;OnlyTitle=1)">下一页</a>'''
    nextUrl = re.compile(reg).findall(html)
    if len(nextUrl) != 0:
        return nextUrl[0]
    reg = '''<a href="(http://www.cnblogs.com/'''+userId+'''/default.html\?page=\d+)">下一页</a>'''
    nextUrl = re.compile(reg).findall(html)
    if len(nextUrl) != 0:
        return nextUrl[0]+'&OnlyTitle=1'
    return None
    
def countPost(userId,nick):
    url = DOMAIN + "/" + userId + '/default.html?OnlyTitle=1'
    html = getHtml(url)
    postCount,commentCount = getCountByScan(html,nick)
    nextUrl = getNextHomePageUrl(html,userId)
    while nextUrl != None:
        html = getHtml(nextUrl)
        postTempCount,commentTempCount = getCountByScan(html,nick)
        postCount += postTempCount
        commentCount += commentTempCount
        nextUrl = getNextHomePageUrl(html,userId)
    return postCount,commentCount

def getBasicInfo(userId):#获取昵、随笔数量、评论数量
    try:
        url = DOMAIN +"/"+userId
        html = getHtml(url)
        #print html
        nick = getNick(html)
        nums = getPostAndCommentNum(html)
        if nums == None:
            nums = countPost(userId,nick)
        return nick,nums
    except Exception as e:
        print e
        return None
    

def login():
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
    parms = {'__EVENTARGUMENT':'','__EVENTTARGET':'',
             '__EVENTVALIDATION':'/wEdAAUyDI6H/s9f+ZALqNAA4PyUhI6Xi65hwcQ8/QoQCF8JIahXufbhIqPmwKf992GTkd0wq1PKp6+/1yNGng6H71Uxop4oRunf14dz2Zt2+QKDEIYpifFQj3yQiLk3eeHVQqcjiaAP',
             '__VIEWSTATE':'/wEPDwULLTE1MzYzODg2NzZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQtjaGtSZW1lbWJlcm1QYDyKKI9af4b67Mzq2xFaL9Bt',
             'btnLogin':'登 录',
             'tbPassword':'**************',
             'tbUserName':'**************',
             'txtReturnUrl': 'http://home.cnblogs.com/',
             }
    loginUrl = "http://passport.cnblogs.com/login.aspx"
    login = urllib2.urlopen(loginUrl,urllib.urlencode(parms))

def getUserInfo():
    seedId = 'fengfenggirl'
    ignoredUser = set()
    unVistedUser = set()
    unVistedUser.add(seedId)
    login()
    saveFile = open('friendship.txt','w')
    count = 0
    while len(unVistedUser) > 0:
        userId = unVistedUser.pop()
        print userId
        if userId not in ignoredUser:
            basicInfo = getBasicInfo(userId)
            if None == basicInfo:
                ignoredUser.add(userId)
                continue
            followees = getFollowees(userId)
            followers = getFollowers(userId)
            string = userId+":"+basicInfo[0]+"\t"+str(basicInfo[1][0])+"\t"+str(basicInfo[1][1])+"\t"
            string += str(len(followees))+"\t"
            for each in followees:
                unVistedUser.add(each)
                string += each+" "
            string = string[0:-1]+"\t"
            string += str(len(followers))+"\t"
            for each in followers:
                unVistedUser.add(each)
                string += each+" "
            string = string[0:-1]
            saveFile.write(string+"\n")
            saveFile.flush()
            if count > 50:
                break
            count += 1
    saveFile.close()
def saveCrawState(visted,queue,vistedFileName = 'visted.txt',queueFileName='queue.txt'):
    vistedFile = open(vistedFileName,'w')
    for each in visted:
        vistedFile.write(each+"\n")
    vistedFile.flush()
    vistedFile.close()
    queueFile = open(queueFileName,'w')
    for each in queue:
        queueFile.write(each+"\n")
    queueFile.flush()
    queueFile.close()
    
def getLastCrawState(vistedFileName = 'visted.txt',queueFileName='queue.txt'):
    vistedFile = open(vistedFileName,'r')
    visted = vistedFile.read().split('\n')
    if len(visted[-1]) == 0:
        visted.pop()
    vistedFile.close()
    queueFile = open(queueFileName,'r')
    queue = queueFile.read().split('\n')
    if len(queue[-1]) == 0:
        queue.pop()
    queueFile.close()
    return set(queue),set(visted)
    
def getFriendship():

    login()
    #vistedUser = set()
    #unVistedUser = set()
    #unVistedUser.add('fengfenggirl')

    unVistedUser,vistedUser = getLastCrawState()
    saveFile = open('friendships.txt','a+')
    count = 4506
    while len(unVistedUser) > 0:
        userId = unVistedUser.pop()
        if userId not in vistedUser:            
            print userId
            try:
                followees = getFollowees(userId)
                followers = getFollowers(userId)
            except Exception as e:
                print e
                unVistedUser.add(userId)#try again
                continue
            vistedUser.add(userId)
            string = userId+":"
            string += str(len(followees))+"\t"
            for each in followees:
                unVistedUser.add(each)
                string += each+" "
            string = string[0:-1]+"\t"
            string += str(len(followers))+"\t"
            for each in followers:
                unVistedUser.add(each)
                string += each+" "
            string = string[0:-1]
            saveFile.write(string+"\n")            
            count += 1
            if count % 300 == 0:
                saveFile.flush()
                saveCrawState(vistedUser,unVistedUser)
                print count,'sleep 60 seconds'
                time.sleep(60)
                    
    saveFile.close()
        
def getFans():
    login()
    vistedUser = set()
    unVistedUser = set()
    unVistedUser.add('fengfenggirl')
    saveFile = open('fans.txt','w+')
    count = 0
    while len(unVistedUser) > 0:
        userId = unVistedUser.pop()
        if userId not in vistedUser:
            print userId
            followers = getFollowers(userId)
            string = userId + "\t"
            for each in followers:
                unVistedUser.add(each)
                string += each+" "
            string = string[0:-1]
            saveFile.write(string+"\n")
            count += 1
            if count % 300 == 0:
                print count,'sleep 60 seconds'
                saveCrawState(vistedUser,unVistedUser,'vFans.txt','qFans.txt')
                time.sleep(60)
                saveFile.flush()
            
    saveFile.close()

if __name__ == "__main__":
    getFriendship()
    #login()
    #userId = 'rubylouvre'
    #print getBasicInfo(userId)
    #followees = getFollowees(userId)
    #print len(followees)
    #print followees
    #print len(getFollowers(userId))
