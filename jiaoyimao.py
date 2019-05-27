# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

import json, time
RANK_PAGE = 'https://xuanchuan.jiaoyimao.com/p/q/dailian1?acti=xy080&from=xy080'
GOODS_PAGE = 'https://m.jiaoyimao.com/seller/goodslist?cateStatus=cateonsold'

COOKIES = json.load(open('liebao.json', encoding='utf-8-sig'))

browser = webdriver.Chrome()
browser.implicitly_wait(10)  #全局等待
browser.get(GOODS_PAGE)  #必须先看一下才行
for c in COOKIES:
    browser.add_cookie(c)
browser.get(GOODS_PAGE)

#点所有商品


def downgoods(link):
    browser.get(link)
    browser.find_element_by_class_name('btn-metro').click()
    browser.find_element_by_class_name('current').click()
    print('下架成功')


def upgoods(link):
    browser.get(link)
    browser.find_element_by_class_name('current').click()
    browser.find_element_by_id('submitGoodsBasicInfo').click()
    browser.find_element_by_id('submitAccountInfo').click()
    return browser.find_element_by_class_name('module-title').text


def loadmore():
    loadmore = browser.find_element_by_id('loadMore')

    while loadmore.is_displayed():

        loadmore.click()
        time.sleep(0.3)
        # loadmore = browser.find_element_by_id('loadMore')


loadmore()
allgoods = []


#得到所有商品 表
def getallgoods():
    goods = browser.find_elements_by_class_name('sell-price')

    for g in goods:
        name: str = g.find_element_by_class_name('name').text
        if '】' not in name:
            continue
        if '段位代练' not in name:
            continue
        game: str = g.find_element_by_class_name('server').text
        link: str = g.find_element_by_class_name('link').get_attribute('href')

        goodsid: str = link.split('/')[-1]
        game = game.split('>')[0].strip()

        ns = name.split('】')[1].split('-')
        ts = name.split('】')[0].split('【')[1].split('-')
        goodstype = ''
        platform = ''
        if len(ts) > 1:
            goodstype = ts[0]
            platform = ts[1]

        if len(ns) < 2:
            print("err", ns, name)
            continue
        start = ns[0]
        end = ns[1]

        allgoods.append({
            'goodstype': goodstype,
            'platform': platform,
            'start': start,
            'end': end,
            'game': game,
            'goodsid': goodsid,
            'link': link
        })


getallgoods()
#去查找游戏区 比对 是不是第一名
for goods in allgoods:
    # print(goods)

    browser.get(RANK_PAGE)
    #claimSegment

    claimSegment = browser.find_element_by_class_name('claimSegment')
    #//*[@id="ant-render-id-_component_52xorarr81vf1ug"]/div/div[2]/div[1]/div[2]/div[1]/div
    tmp = claimSegment.find_elements_by_tag_name('p')
    selm: WebElement = tmp[0]
    eelm: WebElement = tmp[1]
    ultmp = claimSegment.find_elements_by_tag_name('ul')
    selm_li = ultmp[0].find_elements_by_tag_name('li')
    eelm_li = ultmp[1].find_elements_by_tag_name('li')
    try:
        #点击开始等级
        selm.click()
        for li in selm_li:
            if li.text == goods['start']:
                li.click()
                break
        #点击结束等级
        eelm.click()
        for li in eelm_li:
            if li.text == goods['end']:
                li.click()
                break
        btn = browser.find_element_by_class_name('priceBtn')
        #提交
        # browser.implicitly_wait(10)
        btn.click()

        #得到列表 看看是不是第一名
        items = browser.find_elements_by_class_name('goods-item')
        # print(items.count)
        # while len(items) == 0:
        # items = browser.find_elements_by_class_name('goods-item')
        link = items[0].find_element_by_tag_name('a').get_attribute('href')
        if goods['goodsid'] not in link:
            print('落后')
            #下架
            downgoods(goods['link'])
            #上架
            print(upgoods(goods['link']))

    except:
        print(goods)
        continue

print('所有商品检查成功')
browser.quit()