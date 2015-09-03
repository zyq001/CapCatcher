#coding=utf-8
#!/usr/bin/env  python  

import wx
import mechanize
import cookielib
import cStringIO, urllib2
import threading,re,time,os,thread
import urllib
import sys,random
import sitecustomize
import nThread, nClient, globalVal

#import a1,a2,a3,a4,a5

nameList = ['a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
tempName = 'a1.png'
tempCode = ''
image = wx.Image('a0.png', wx.BITMAP_TYPE_ANY)
name = 'chenyun'
threadcount = 5
#刷新客户端类，有刷新get和提交summit两个方法

    
if __name__ == '__main__':
    name = raw_input('mingzi:')
    progcount = input('zu shu:')
    threadcount = input('xiancheng shu:')
    #print('?????????????')
    #c创建窗口
    app = wx.PySimpleApp()
    frame = TextEnter(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
