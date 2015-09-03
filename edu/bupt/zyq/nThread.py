__author__ = 'Administrator'
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
import nClient

class TextEnter(wx.Frame):
    def __init__(self, parent, id):
        global progcount
        global threadcount
        global image
        wx.Frame.__init__(self,parent,id, 'Text Test', size=(300,200))
        self.panel = wx.Panel(self)
        self.enterText = wx.TextCtrl(self.panel, -1, "", size=(175, -1),style=wx.TE_PROCESS_ENTER)
        self.enterText.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter,self.enterText)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.fgs = wx.FlexGridSizer(cols=2, hgap=10,vgap=10)
        image = wx.Image('a0.png', wx.BITMAP_TYPE_ANY)
        self.sb1 = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(image))
        #wx.StaticBitmap(parent=panel,bitmap=temp)
        self.fgs.Add(self.sb1)
        self.fgs.Add(self.enterText)
        self.panel.SetSizerAndFit(self.fgs)
        self.Fit()
        self.threads = []#线程池
        self.pics = []#图片名称库
        print(u'窗口初始化完成')
        #客户端实例

        for i in range(1,threadcount+1):
            userAgent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.'+str(progcount)+'.'+str(i)
            picname = 'a'+str(i)+'.png'
            self.pics.append(picname)
            t = nThread(userAgent, picname)
            t.start()
            print (u'线程', i, u'启动')
            self.threads.append(t)

    #UI窗口关闭的时候退出子线程
    def OnCloseWindow(self, evt):
        for thread in self.threads:
            thread.Stop()
        self.Destroy()

    def onEnter(self, event):
        global image
        global nameList
        global tempName#上次的图片名称
        global tempCode#此次的验证码，用与下次比较判断是否重复
        flag = False#标示量：是否遍历找到图片
        if self.enterText.GetValue() not in ['', tempCode]:#输入框提交不为空，并且不与上次提交相同
            #在新线程中向服务器提交，并查找次验证码之后是否有新的，如有则在界面中显示
            tempCode = self.enterText.GetValue()#记录此次输入，以留作判定
            print(tempCode)
            indexLast = self.pics.index(tempName)#当前图片下标
            thread1 = self.threads[indexLast]
            thread1.nClient.summit(tempCode)
            if indexLast != (len(self.pics)-1):
                for thread in self.threads[indexLast+1:]:#遍历上次图片之后的序列
                    if thread.nClient.ready == True:
                        image = wx.Image(thread.nClient.picName, wx.BITMAP_TYPE_ANY)
                        tempName = thread.nClient.picName
                        flag = True
                        break

        #如果后半部分找到新的，直接UI界面刷新图片，并且函数return
        if flag == True:
            try:
                self.sb1 = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(image))
                self.panel.SetSizerAndFit(self.fgs)
            except wx._core.PyAssertionError:
                pass
            self.Fit()
            self.panel.Refresh()
            #self.enterText.Clear()#清空输入框
            self.enterText.Clear()#清空输入框
            return
        #清空输入框
        self.enterText.Clear()
        #print(u'清空')

        #该验证码之后没有找到新的，或第一次启动时，循环遍历寻找并显示，找到后刷新返回,
        #不找最后一个是因为大多数情况这块是输入完最后一个后被调用
        for thread in self.threads:
            if thread.nClient.ready == True:
                try:
                    image = wx.Image(thread.nClient.picName, wx.BITMAP_TYPE_ANY)
                #except wx._core.PyAssertionError:
                except :
                    pass

                tempName = thread.nClient.picName
                try:
                    self.sb1 = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(image))
                    self.panel.SetSizerAndFit(self.fgs)
                #except wx._core.PyAssertionError:
                except :
                    pass
                self.Fit()
                self.panel.Refresh()
                flag = True
                return#找到之后更新图片，然后跳出函数
        print(u'部分遍历完成')

        #如果还未找到新图片，放上wait图片，然后持续检查是否有新验证码
        try:#没找到，
            tempName = 'wait.png'
            image = wx.Image(tempName, wx.BITMAP_TYPE_ANY)
            #print(u'tempName变为wait.png')
        except wx._core.PyAssertionError:
           # print(u'image的问题？')
            pass

        try:
            self.sb1 = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(image))
            self.panel.SetSizerAndFit(self.fgs)
        except wx._core.PyAssertionError:
            pass
        self.Fit()
        self.panel.Refresh()
        #持续检查
        print(u'wait图片加载完成')
        while not flag:
            #try:
            for thread in self.threads:
                if thread.nClient.ready == True:
                    tempName = thread.nClient.picName
                    #time.sleep(1)
                    try:
                        image = wx.Image(tempName, wx.BITMAP_TYPE_ANY)
                   # except wx._core.PyAssertionError:
                      #  pass
                    except:
                        pass
                    try:
                        self.sb1 = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(image))
                        self.panel.SetSizerAndFit(self.fgs)
                    except :
                        pass
                    self.Fit()
                    self.panel.Refresh()
                    flag = True
                    return#找到之后更新图片，然后跳出函数
           # except:
             #   pass
            print(u'持续获取中....')
            time.sleep(2)