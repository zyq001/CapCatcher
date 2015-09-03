#coding=utf-8
#!/usr/bin/env  python  
__author__ = 'Administrator'
import wx
import mechanize
import cookielib
import cStringIO, urllib2
import threading,re,time,os,thread
import urllib
import sys,random
import sitecustomize
import globalVal

class nClient():
    def __init__(self, Useragent, picName):
        global name
        self.ready = False
        self.picName = picName
        self.Url1 = 'http://54.245.51.239:8153/?name='+name
        self.Url = 'http://54.245.51.239:8153/'
        self.br = mechanize.Browser()
        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        # Browser options
        self.br.set_handle_equiv(True)
        #br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        # User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent', Useragent)]
        print(u'===============client初始化成功')
        while True:#保证打开带名字的网址，已完成注册，并将cookie叫给cj
            try:
                resp1 = self.br.open(self.Url1)
            except urllib2.URLError:
                print(u'================注册名字出错')
                print(name+u'================可能服务器还未开')
                pass
            else:
                print(u'================注册名字成功')
                break
    def get(self):
        while not self.ready:#当前目录没有该图片即刷新
            while True:
                try:
                    resp = self.br.open(self.Url)
                    break
                except urllib2.URLError:
                    print(u'=================刷新出错')
                    pass
            html = resp.read()
            #print(html)
            imgurl = re.search('<img src="(.+?)"/>', html)
            if imgurl:
                Imgurl = imgurl.group(1)
                try:
                    res=urllib.urlretrieve(self.Url+Imgurl, self.picName)
                except IOError:
                    print(u'============下载图片出错===========================')
                    pass
                self.ready = True
                return
            else: # 网页中没有图片
                continue

    def summit(self, code):
        #print self.br.form
        #for form in self.br.forms():
         #   print form
        try:
            self.br.select_form(nr=0)
            self.br.form['captcha']=code
            self.br.submit()
        except urllib2.URLError:
            print(u'=========提交出错===========')
            pass
        #respS = self.br.submit()
        #print (respS)
        #print(respS.read())
        try:
            os.remove(self.picName)
        except WindowsError:
            print(u'===============删除图片出错')
            pass
        self.ready = False

