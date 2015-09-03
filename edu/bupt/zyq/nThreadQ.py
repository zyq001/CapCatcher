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

class nThreadQ(threading.Thread):
    def __init__(self, window, Useragent,picName):
        self.flag = True
        threading.Thread.__init__(self)
        self.nClient = nClient(Useragent,picName)
        self.pic = picName
        self.ready = self.nClient.ready
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.timeToQuit.clear()
    def run(self):
        while self.flag:
            self.nClient.get()
            if self.nClient.ready == True:
                wx.CallAfter(self.window.addToSque, self.pic)
                print('call le')
                while self.nClient.ready:
                    time.sleep(0.1)
                    continue
            #time.sleep(0.1)
    def Stop(self):
#self.timeToQuit.set()
        self.flag = False
        print(u'==================线程退出=============')