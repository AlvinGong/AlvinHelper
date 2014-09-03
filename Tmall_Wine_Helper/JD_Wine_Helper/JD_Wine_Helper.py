from selenium import webdriver
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
    count = '1'
    years = ''

    @staticmethod
    def GetSchema():
        return ['title','price','link','page','comments_count',\
            'activity', 'capacity', 'vol', 'count', 'years']

class JDWineHelper():
    url = r'http://list.jd.com/list.html?cat=12259%2C12260%2C9435&delivery=1&page=1&JL=4_10_0'
    dirName = 'jd'

    def GetWineInfo(self, url='', dirName=''):
        if url:
            self.url = url
        if dirName:
            self.dirName = dirName
        driver = webdriver.Firefox()
        driver.get(self.url)
        if not os.path.exists(self.dirName):
            os.makedirs(self.dirName)
        if not os.path.exists('{0}//{1}'.format(self.dirName, aUtil.GetFileNameFromDate())):
            os.makedirs('{0}//{1}'.format(self.dirName, aUtil.GetFileNameFromDate()))
        while(1):
            while(not self.IsNormalPage(driver)):
                print('Warning: "{0}" is NOT Normal Page. Will revisit it again after 10 seconds...'.format(self.url))
                time.sleep(10)
                driver.get(self.url)
            print('Reading {0}...'.format(self.url))
            ofile = open('{0}//{1}//{2}.csv'.format(self.dirName, aUtil.GetFileNameFromDate(),self.getPageNum(self.url)),'w')
            ofile.writelines('haha')
            try:
                writer = csv.writer(ofile, dialect='excel', delimiter='\t')
                writer.writerow(WineInfo.GetSchema())
                self.GetWinesFromTargetPage(driver,writer)
                #writer.close()
            except Exception as e:
                print('!!!Error: Exception!!!')
                print(e)
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

    def GetDryFruitsInfo(self, url='', dirName=''):
        page = 1
        if url:
            self.url = url + str(page)
        if dirName:
            self.dirName = dirName
        driver = webdriver.Firefox()
        driver.get(self.url)
        if not os.path.exists(self.dirName):
            os.makedirs(self.dirName)
        if not os.path.exists('{0}//{1}'.format(self.dirName, aUtil.GetFileNameFromDate())):
            os.makedirs('{0}//{1}'.format(self.dirName, aUtil.GetFileNameFromDate()))
        
        while(1):
            while(driver.current_url == self.url and driver.current_url != url):
                time.sleep(2)
            self.url = driver.current_url
            while(not self.IsNormalPage(driver)):
                print('Warning: "{0}" is NOT Normal Page. Will revisit it again after 10 seconds...'.format(self.url))
                time.sleep(10)
                driver.get(self.url)
            print('Reading {0}...'.format(self.url))
            ofile = open('{0}//{1}//{2}.csv'.format(self.dirName, aUtil.GetFileNameFromDate(),self.getPageNum(self.url)),'w')
            ofile.writelines('haha')
            try:
                writer = csv.writer(ofile, dialect='excel', delimiter='\t')
                writer.writerow(WineInfo.GetSchema())
                self.GetDryFruitsFromTargetPage(driver, writer)
                #writer.close()
            except Exception as e:
                print('!!!Error: Exception!!!')
                print(e)
            ofile.close()
            #break # For debug
            if self.IsLastPage(driver):
               break
            else:
                #self.GetNextBtn(driver).send_keys('{RIGHT}')
                self.GetNextBtn(driver).click()
                #nextBtn.click()
                #page = page + 1
                #self.url = url + str(page)
            print('Finished...')
            #break
            time.sleep(5)
            driver.set_page_load_timeout(30)
            #try:
            #    driver.get(self.url)
            #except TimeoutException as te:
            #    print("Timeout Exception Captured...")
            #    driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop")')
            
        driver.close()

    def getPageNum(self, url):
        paras = url.split('&')
        name = 'page=unknown'
        for para in paras:
            if para.startswith('page='):
                name = para
        return name
    
    def IsNormalPage(self, driver):
        return (self.url.startswith(r'http://list.jd.com/list.html') or self.url.startswith(r'http://search.jd.com/Search'))

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

    def MergeFiles(self, dirName=''):

        if dirName:
            self.dirName = dirName
        if not os.path.exists(self.dirName):
            os.makedirs(self.dirName)
        if not os.path.exists('{0}//{1}'.format(self.dirName, aUtil.GetFileNameFromDate())):
            os.makedirs('{0}//{1}'.format(self.dirName, aUtil.GetFileNameFromDate()))
        try:
            oSummary = open('{0}//{1}.csv'.format(self.dirName, aUtil.GetFileNameFromDate()),'w')
            hasHead = 0
            for line in os.popen('dir /b /s {0}\\{1}'.format(self.dirName, aUtil.GetFileNameFromDate())):
                filePath = line.rstrip()
                for item in open(filePath, 'r'):
                    if(re.search('^hahatitle', item) != None and hasHead == 1):
                        continue
                    if(item == '\n' or item == ''):
                        continue
                    oSummary.write(item)
                    hasHead = 1
                print('Merging {0}...'.format(line))
        except Exception as e:
            print(e)
        finally:
            oSummary.close()

    def GetDryFruitsFromTargetPage(self, driver, writer):
        #driver = webdriver.Firefox()
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(3)
        htmWines = driver.find_elements_by_css_selector('#plist li')
        for htmWine in htmWines:
            wine = WineInfo()
            wine.page = driver.current_url
            
            try:
                wine.title = htmWine.find_element_by_css_selector('.p-name').text
            except:
                continue
            try:
                wine.activity = htmWine.find_element_by_css_selector('.p-name .adwords').text
                wine.title = wine.title.replace(wine.activity,'')
            except:
                wine.activity = ''
            print(wine.title)
            caps = re.search('\d+((千克)|g|克|(kg))', wine.title.lower())
            wine.capacity = caps.group(0) if not caps is None else ''
            counts = re.search('\d+袋',wine.title)
            wine.count = counts.group(0) if not counts is None else '1'
            wine.price = htmWine.find_element_by_css_selector('.p-price strong').text
            wine.link = htmWine.find_element_by_css_selector('.p-name a').get_attribute('href')
            wine.page = self.getPageNum(self.url)
            txtComment = htmWine.find_element_by_css_selector('.extra a').text
            comments = re.search('\d+人',txtComment)
            wine.count_comments = comments.group(0) if not comments is None else 'NA'
            wine.count_comments = wine.count_comments.replace(r'人','')
            writer.writerow([wine.title,wine.price,wine.link,\
                wine.page,wine.count_comments,wine.activity,\
                wine.capacity,wine.vol,wine.count,wine.years])
        

jdHelper = JDWineHelper()
#jdHelper.GetWineInfo()
#jdHelper.GetWineInfo(r'http://list.jd.com/list.html?cat=12259%2C12260%2C9438&delivery=1&page=1&JL=4_10_0', r'RedWine')
#jdHelper.GetWineInfo(r'http://list.jd.com/list.html?cat=12259%2C12260%2C9436&delivery=1&page=1&JL=4_10_0', r'YellowWine')
jdHelper.GetDryFruitsInfo(r'http://search.jd.com/Search?keyword=%E6%9E%9C%E5%B9%B2&enc=utf-8#keyword=%E6%9E%9C%E5%B9%B2&enc=utf-8&qr=&qrst=UNEXPAND&et=&rt=1&click=&psort=&page=',r'DryFruits')


#folder = r'C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\DryFruits\2014-09-01'
#log = r'C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\DryFruits\DryFruits.csv'
#for line in os.popen(r'dir /b /l C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\DryFruits\2014-09-01'):
#    filePath = folder + "\\" + line
jdHelper.MergeFiles(r'C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\DryFruits')

##jdHelper.MergeFiles(r'C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\jd')
##jdHelper.MergeFiles(r'C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\RedWine')
##jdHelper.MergeFiles(r'C:\Users\Public\Documents\ByteMe\Tmall_Wine_Helper\JD_Wine_Helper\YellowWine')
#os.popen('shutdown -f -s -t 30')
    

