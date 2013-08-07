#-*- coding=utf-8 -*-
import time,urllib2,urllib,re,HTMLParser,os
from htmlentitydefs import entitydefs


class PageParser(HTMLParser.HTMLParser):#翻译实体
    def __init__(self):
        self.data=""
        self.readcode=0
        HTMLParser.HTMLParser.__init__(self)
    def handle_starttag(self,tag,attrs):
        if tag=='textarea':
            self.readcode=1
    def handle_data(self,data):
        if self.readcode:
            self.data+=data
    def handle_endtag(self,tag):
        if tag=='textarea':
            self.readcode=0
    def handle_entityref(self,name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name])
    def getdata(self):
        return self.data
 
global res
def getACUrl():
    step=1
    r=re.compile(unicode("下一页","utf8"))
    #.{500}?\"
    r2=re.compile("<input type=\"hidden\" name=\"__VIEWSTATE\" id=\"__VIEWSTATE\" value=\".{1,50000}?\" />")
    url = "http://algorithm.fzu.edu.cn/OnlineJudgeUserStatus.aspx"
    parms = {
        '__EVENTTARGET':'ctl00$MainRightHolder$UserStatusGridView',
        'ctl00$MainRightHolder$UserIdTextBox':'120320050',
        }
    login1=urllib2.urlopen(url)
    pagedata=login1.read()
    s1=r2.findall(pagedata)
    if len(s1)==0:
        return
    parms['__VIEWSTATE']=s1[0][64:-4]#form表单的提取
    while True:
        try:
            if step==1:
                parms['__EVENTARGUMENT']='Page$First'
            else:
                parms['__EVENTARGUMENT']='Page$Next'
            step+=1
            login = urllib2.urlopen(url,urllib.urlencode(parms))
            data=(unicode(login.read(),"utf8"))
            #            fout=open("c:\\1.html","wb+")
            #            fout.write(data.encode("GBK"))
            #            fout.close()
            findurl(data)
            if len(r.findall(data))==0:
                break
            s1=r2.findall(data)
            if len(s1)==0:
                return
            parms['__VIEWSTATE']=s1[0][64:-4]
            data=""
        except Exception,e:
            print(e)
            break
def Login(username,password):#模拟登陆
    try:
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        urllib2.install_opener(opener)
        parms = {
            '__VIEWSTATE':r'/wEPDwULLTE2ODk5MTAyOTUPZBYCAgMPZBYCAgUPEA8WAh4LXyFEYXRhQm91bmRnZBAVCAzmnIDmlrDkv6Hmga8S566X5rOV6ICD6K+V6YCa55+lG+esrOS4g+asoeS9nOS4muebuOWFs+mXrumimCQxMuaciDXml6Xnrpfms5Xor77lgZzkuIrkuIDmrKHvvIzor74S5LyY56eA5L2c5Lia5YCZ6YCJKCDlhbPkuo7popjnm67nmoTml7bpl7Tnqbrpl7TpmZDliLbnmoTpl64k5YWz5LqO55m76ZmG57O757uf55So5oi35ZCN5LiO5a+G56CBCD4+5pu05aSaFQgAF1Nob3dCdWxsZXRpbi5hc3B4P2JpZD04F1Nob3dCdWxsZXRpbi5hc3B4P2JpZD03F1Nob3dCdWxsZXRpbi5hc3B4P2JpZD01F1Nob3dCdWxsZXRpbi5hc3B4P2JpZD00F1Nob3dCdWxsZXRpbi5hc3B4P2JpZD0zF1Nob3dCdWxsZXRpbi5hc3B4P2JpZD0yEUJ1bGxldGluTGlzdC5hc3B4FCsDCGdnZ2dnZ2dnFgBkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRJCYW5uZXIkTG9naW5CdXR0b24FIEJhbm5lciRVc2VyQ29udHJvbFBhbmVsTXVsdGlWaWV3Dw9kZmSAQToRVgZ7Ntt6y/9+2cO87+ENUvmluX16Ns5f0y+0Kw==',
            'Banner$LoginButton.x':'17',
            'Banner$LoginButton.y':'5'
        }
        parms[r"Banner$UserNameText"]=username
        parms[r"Banner$Password"]=password

        loginUrl = "http://algorithm.fzu.edu.cn/Default.aspx"
        login = urllib2.urlopen(loginUrl,urllib.urlencode(parms))
        h=(unicode(login.read(),"utf8"))
        # loginer = urllib2.urlopen("http://poj.org/")#登录主页
        #  print(loginer.read().decode("utf8"))
    except Exception,e:
        print(e)
def findurl(data):
    r=re.compile("<a class=\"underline\" href=\".{1,500}?\" target=\"_blank\">.{1,500}?</a></td><td><a class=\"hover-underline\" href=\".{1,500}?\" target=\"_blank\">AC\|AC\|AC\|AC\|AC\|AC\|AC\|AC\|AC\|AC\|</a>")
    h=r.findall(data)
    import string
    global res
    for s in h:
        y=string.find(s,"cpp")
        if y==-1:
            continue
        x=y
        while(s[x]!='>'):
            x-=1
        name=s[x+1:y+3]
        if name in res.keys():
            continue
        x=string.find(s,"href=")
        if x==-1:
            continue
        y=string.find(s,"\" target=")
        if y!=-1:
            ss=s[x+6:y]
            x=string.find(ss,"&")
            if x!=-1:
                ss="http://algorithm.fzu.edu.cn/"+ss[:x+1]+ss[x+5:]
                res[name]=ss
def getACUrl2():
    r=re.compile("<a target='_blank' href='.{1,500}?'>.{1,500}?</a></td><td>AC\|AC\|AC\|AC\|AC\|AC\|AC\|AC\|AC\|AC\|</td>")
    url = "http://algorithm.fzu.edu.cn/StuMain.aspx"
    try:
        login = urllib2.urlopen(url)
        data=(unicode(login.read(),"utf8"))
        h=r.findall(data)
        import string
        global res
        for s in h:
            x=string.find(s,"cpp")
            if x==-1:
                continue
            y=x
            while x>0 and s[x]!='>':
                x-=1
            if x<0:
                continue
            name=s[x+1:y+3]
            if name in res.keys():
                continue
            t=y
            y=x
            x=t
            while not( x>4 and s[x]=='=' and s[x-1]=='f' and s[x-2]=='e' and s[x-3]=='r' and s[x-4]=='h'):
                x-=1
            if x==-1:
                continue
            while y>=0 and s[y]!='\'':
                y-=1
            if y<0:
                continue
            res[name]="http://algorithm.fzu.edu.cn/"+s[x+2:y]
    except Exception,e:
        print(e)
if __name__ == '__main__':
    username=raw_input("请输入用户名:")
    password=raw_input("请输入密码:")
    global res
    res={}
    Login(username,password)#模拟登陆
    getACUrl2()#获取管理后台中的AC代码
    getACUrl()#获取AC代码对应的url
    if not os.path.exists("ACCode"):
        os.mkdir("ACCode")
    for key in res:
        print key
        u=urllib2.urlopen(res[key])#根据获取的url，逐个访问，并将代码保存到本地
        pp=PageParser()
        pp.feed(u.read())
        data=pp.getdata()
        fout=open('ACCode'+'\\'+key,"wb+")
        fout.write(data)
        fout.close()
    print "共%d份AC代码" % len(res)
