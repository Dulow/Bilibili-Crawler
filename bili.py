import re
import sys
import urllib
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import threading
import queue
from urllib import request

class myThread(threading.Thread):
    def __init__(self,threadID,urlq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.urlq = urlq
        #self.threadout = threadout
    def run(self):
        while True:
            #name = self.threadID.get()
            a = []
            purl = queue.Queue.get(self.urlq)
            a = (get_up_data(purl))
            save_data_in_db(a)
            '''
            #print(type(purl))
            #print(purl)
            #js = 'window.open("{}");'.format(purl)
            #print(js)
            #js='window.open(%s);'%purl
            #js='window.open("https://www.sogou.com");'
            #print(js)
            #driver.execute_script(js)
            #driver.switch_to_window(driver.window_handles[int(self.threadID)])
            #driver = webdriver.new.Chrome('D:/Python/chromedriver/chromedriver.exe')
            driver.get(purl)
            time.sleep(2)
            follow = driver.find_element_by_id('n-gz')
            fans =  driver.find_element_by_id('n-fs')
            the_id = 'n-bf'
            if is_element_existid(the_id) == True:
                plays = driver.find_element_by_id('n-bf')
                playnum = play.text
            else:
                playnum = '0'
            print(follow.text,fans.text,playnum)
            #try :
            #get_up_datas(purl)
            #except:
                #print('can not get data')
            '''

def is_element_existid(the_id):
    try:
        driver.find_element_by_id(the_id)
        return True
    except:
        return False

#
def creat_table():
    db = pymysql.connect('localhost','root','ck','bili',charset='utf8')
    sql = "create table if not EXISTS up_data (\
                                id int(15) not null auto_increment,\
                                name varchar(200) not null,\
                                follow varchar(20),\
                                fans varchar(20),\
                                playnum varchar(20),\
                                primary key(id))ENGINE=InnoDB DEFAULT CHARSET=utf8"
    cur = db.cursor()
    cur.execute(sql)
    cur.close()
    db.close()

def save_data_in_db(A):
    n = str(A[0])
    #print(type(n))
    fo = str(A[1])
    fa = str(A[2])
    p = str(A[3])
    db = pymysql.connect('localhost','root','ck','bili',charset="utf8")
    sql = """insert into up_data (
            name,follow,fans,playnum)
            values(%s,%s,%s,%s)"""

    cursor = db.cursor()
    cursor.execute("""insert into up_data (
            name,follow,fans,playnum) values(%s,%s,%s,%s)""",(n,fo,fa,p))
    db.commit()
    print('zhixing')
    cursor.close()
    db.close()

def log_in(url):
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="login-app"]/div/div/div[3]/div[3]/div/div/ul/li[6]/a[2]').click()
    time.sleep(3)
    #sreach_window = driver.current_window_handle
    #wait = WebDriverWait(driver,10)
    try:
        driver.switch_to_window(driver.window_handles[0])
        driver.switch_to_frame('ptlogin_iframe')
        driver.find_element_by_id('switcher_plogin').click()
        time.sleep(1)
        driver.find_element_by_id('u').send_keys('1393116635')
        time.sleep(1)
        driver.find_element_by_id('p').send_keys('54250385425038ha')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="login_button"]').click()
        time.sleep(5)
        cookie = driver.get_cookies()
        #driver.quit()
    except TimeoutError:
        print('Can not log in')
    #return cookie
'''
def add_cookies(cookie):
    #向session添加cookies
    c = requests.cookies.RequestsCookieJar()
    for i in cookie:
        c.set(i['name'],i['value'])
    s.cookies.update(c)
'''

def get_up_data(urls):  #,header):
    #header = header
    #req = s.get(urls)
    #soup = BeautifulSoup(req.content,'html.parser')
    #print(soup)
    c = []
    driver.get(urls)
    time.sleep(3)
    nam = driver.find_element_by_id('h-name')
    name = nam.text
    #print(type(name))
    foll = driver.find_element_by_id('n-gz')
    follow = foll.text
    fan =  driver.find_element_by_id('n-fs')
    fans = fan.text
    the_id = 'n-bf'
    if is_element_existid(the_id) == True:
        plays = driver.find_element_by_id('n-bf')
        playnum = plays.text
    else:
        playnum = '0'
    print(name,follow,fans,playnum)
    c = [name,follow,fans,playnum]
    return c


if __name__ == '__main__':
    urlq = queue.Queue()
    header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/'
                  '535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    }
    purl = "https://passport.bilibili.com/login"
    #首页url
    #s = requests.session()#新建session
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    #driver = webdriver.Chrome(chrome_options=chrome_options,executable_path = "D:/Python/chromedriver/chromedriver")
    driver = webdriver.Chrome("D:/Python/chromedriver/chromedriver.exe")
    creat_table()
    log_in(purl)
    #add_cookies(theone)
    for i in range(1550162):
        d = 'https://space.bilibili.com/' + str(10000000+i)
        urlq.put(d)
        #get_up_data(url,header)
    t1 = myThread(1,urlq)
    t2 = myThread(2,urlq)
    t3 = myThread(3,urlq)
    t1.start()
    urlq.join()
    t2.start()
    urlq.join()
    t3.start()
    urlq.join()
    #for id in a:
    '''
    xpath = '//*[@id="ranking_douga"]/div/ul[1]/li[1]/a/div[2]/p[2]'
    while flag == 0:
        if is_element_exist(xpath) == False:
            driver.execute_script('window.scrollBy(0,100)')
        else:
            test = driver.find_element_by_xpath('//*[@id="ranking_douga"]/div/ul[1]/li[1]/a/div[2]/p[2]')
            flag += 1
    print(test.text)
    '''
