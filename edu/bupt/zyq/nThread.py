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

class nThread(threading.Thread):
    def __init__(self, Useragent,picName):
        self.flag = True
        threading.Thread.__init__(self)
        self.nClient = nClient(Useragent,picName)
        self.ready = self.nClient.ready
    def run(self):
        while self.flag:
            self.nClient.get()
            time.sleep(0.1)
    def Stop(self):
        self.flag = False
        print(u'==================线程退出=============')