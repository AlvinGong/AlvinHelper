﻿from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import *
import time
import csv
import sys
import os
from AlvinUtility import AlvinUtility as aUtil
import re

class WineInfo():
    title = ''
    price = ''
    link = ''
    page = ''
    count_comments = ''
    activity = ''
    capacity = ''
    vol = ''
    count = ''
    years = ''

    @staticmethod
    def GetSchema():
        return ['title','price','link','page','comments_count',\
            'activity', 'capacity', 'vol', 'count', 'years']

class JDWineHelper():
    url = r'http://list.jd.com/list.html?cat=12259%2C12260%2C9435&delivery=1&page=1&JL=4_10_0'

    def Run(self, url=''):
        if url:
            self.url = url
        driver = webdriver.Firefox()
        driver.get(self.url)
        if not os.path.exists('jd'):
            os.makedirs('jd')
        if not os.path.exists('jd//{0}'.format(aUtil.GetFileNameFromDate())):
            os.makedirs('jd//{0}'.format(aUtil.GetFileNameFromDate()))
        while(1):
            while(not self.IsNormalPage(driver)):
                print('Warning: "{0}" is NOT Normal Page. Will revisit it again after 10 seconds...'.format(self.url))
                time.sleep(10)
                driver.get(self.url)
            print('Reading {0}...'.format(self.url))
            ofile = open('jd//{0}//{1}.csv'.format(aUtil.GetFileNameFromDate(),self.getPageNum(self.url)),'w')
            ofile.writelines('haha')
            try:
                writer = csv.writer(ofile, dialect='excel', delimiter='\t')
                writer.writerow(WineInfo.GetSchema())
                self.GetWinesFromTargetPage(driver,writer)
                #writer.close()
            except:
                print('!!!Error: Exception!!!')
            ofile.close()
            #break # For debug
            if self.IsLastPage(driver):
               break
            else:
                self.url = self.GetNextBtn(driver).get_attribute('href')
            print('Finished...')
            #break
            time.sleep(5)
            driver.set_page_load_timeout(30)
            try:
                driver.get(self.url)
            except TimeoutException as te:
                print("Timeout Exception Captured...")
                driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop")')
            
        driver.close()

    def getPageNum(self, url):
        paras = url.split('&')
        for para in paras:
            if para.startswith('page='):
                return para
        return 'page=unknown'
    
    def IsNormalPage(self, driver):
        return self.url.startswith(r'http://list.jd.com/list.html')

    def GetNextBtn(self, driver):
        try:
            nextBtn = driver.find_element_by_css_selector('.next')
        except:
            nextBtn = None
        return nextBtn 

    def IsLastPage(self, driver):
        #driver = webdriver.Firefox()
        return self.GetNextBtn(driver) is None

    def GetWinesFromTargetPage(self, driver, writer):
        #driver = webdriver.Firefox()
        htmWines = driver.find_elements_by_css_selector('#plist li')
        for htmWine in htmWines:
            wine = WineInfo()
            wine.page = driver.current_url
            
            wine.title = htmWine.find_element_by_css_selector('.p-name').text
            try:
                wine.activity = htmWine.find_element_by_css_selector('.p-name .adwords').text
                wine.title = wine.title.replace(wine.activity,'')
            except:
                wine.activity = ''
            print(wine.title)
            caps = re.search('\d+（ml|毫升）', wine.title.lower())
            wine.capacity = caps.group(0) if not caps is None else ''
            uCode = '0xb6'.encode('utf8')
            vols = re.search('\d+度', wine.title)
            wine.vol = vols.group(0) if not vols is None else ''
            counts = re.search('\d+瓶',wine.title)
            wine.count = counts.group(0) if not counts is None else '1'
            years = re.search('[0-9十百一二三四五六七八九]+年',wine.title)
            wine.years = years.group(0) if not years is None else ''
            wine.price = htmWine.find_element_by_css_selector('.p-price strong').text
            wine.link = htmWine.find_element_by_css_selector('.p-name a').get_attribute('href')
            wine.page = self.getPageNum(self.url)
            txtComment = htmWine.find_element_by_css_selector('.evaluate').text
            comments = re.search('\d+人',txtComment)
            wine.count_comments = comments.group(0) if not comments is None else 'NA'
            writer.writerow([wine.title,wine.price,wine.link,\
                wine.page,wine.count_comments,wine.activity,\
                wine.capacity,wine.vol,wine.count,wine.years])

jdHelper = JDWineHelper()
jdHelper.Run()

