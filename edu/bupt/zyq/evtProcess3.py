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

#import a1,a2,a3,a4,a5
import TextEnterQ

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
    frame = TextEnterQ(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
