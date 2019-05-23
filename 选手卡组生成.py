# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import csv
import json
import urllib
from urllib import request
from urllib import parse
import os, shutil
from urllib.request import urlretrieve
if os.path.exists("pic") == False:
    os.mkdir("pic")
from PIL import Image, ImageDraw, ImageFont

word_css = "DFHeiW7.ttf"
font = ImageFont.truetype(word_css, 20)
costfont = ImageFont.truetype(word_css, 30)

outimg = Image.open('bg.jpg')
draw = ImageDraw.Draw(outimg)
cards = []
allcards = json.load(open('cards.json', encoding='utf-8'))


#下载图片 有就跳过,没有就下载
def downloadCardImg(url, filename):
    #print(url)
    fileurl = "pic/" + str(filename) + '.jpg'
    if os.path.exists(fileurl):  #如果存在就不下载
        return fileurl
    urlretrieve('http:' + url, fileurl)
    return fileurl


def downloaddeck(code):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://wiki-sv.netease.com/picker?specify=false&code=' + code)
    pickedlist = driver.find_elements_by_class_name('m-picked-card')

    for card in pickedlist:
        name = card.find_element_by_class_name('name').text.replace('‧', ' ')
        cost = card.find_element_by_class_name('cost').text
        count = card.find_element_by_class_name('quantity').text.replace(
            '×', '')
        cardid = card.find_element_by_class_name('remove').get_attribute(
            'data-card-id')

        picurl = card.get_attribute('style')
        picurl = picurl.replace('");', '').replace('background-image: url("',
                                                   'http:')

        pic = downloadCardImg(picurl, cardid)
        cards.append([cost, name, count, cardid])

    driver.quit()


def getcards(jdata):
    retc = {}
    for c in jdata['data']['cardID']:
        cj = findcard(c)
        #print(cj)
        #print(c)
        downloadCardImg(cj['牌组小图'], cj['url'])
        if c in retc:
            retc[c] = [
                str(cj['cost']), cj['name'],
                int(retc[c][2]) + 1,
                str(c)
            ]
        else:
            retc[c] = [str(cj['cost']), cj['name'], 1, str(c)]

    for c in retc:
        cards.append(retc[c])

    print(cards)


def findcard(cardid):
    for c in allcards:
        if int(c['url']) == int(cardid):
            return c


def drawCard(cost, name, count, id):
    #先打开图片

    cardimg = Image.open('pic/' + id + '.jpg')
    cardimg = cardimg.resize((256, 48), Image.ANTIALIAS)

    cardDraw = ImageDraw.Draw(cardimg)
    #cost
    costbg = Image.open('costbg.png')

    costdraw = ImageDraw.Draw(costbg)
    costdraw.text((7, 0), str(cost), font=costfont)
    cardimg.paste(costbg, (9, 9, 39, 39))

    cardDraw.text((39, 12), name, font=font)
    cardDraw.text((220, 9), 'x' + str(count), font=costfont)
    #cardimg.show()
    return cardimg


def tocards(code):
    data = {
        "deck_code": code,
    }
    postdata = parse.urlencode(data).encode('utf-8')
    jtext = urllib.request.urlopen("https://exp.16163.com/sv/to_cards",
                                   postdata)
    html=jtext.read().decode('utf-8')
    j = json.loads(html)
    return j


#得到json
cardsjson = tocards(
    'AADE8WnyIjY9zKOMX1uFVv5qVJnLBmSn9DUtDYI1myjLGvQ')

print(cardsjson['data']['clan'])#职业
#1精灵  2皇家 3巫师 4龙 5死 6吸 7主 8超

print(cardsjson['data']['deck_format'])#1 是无限   2是指定

#转成数组
getcards(cardsjson)
#按cost排序
cards = sorted(cards, key=lambda x: x[0])

# 画出职业 
#todo 指定/无限
classimg=Image.open('class/'+str(cardsjson['data']['clan'])+'.jpg')
classimg=classimg.resize((256*2, 60*2), Image.ANTIALIAS)
#写出名字
playname_draw=ImageDraw.Draw(classimg)
namefont = ImageFont.truetype(word_css, 35)

playname_draw.text((10,10),"这一定是十个中文字符",font=namefont)

x1,y1=classimg.size
#todo 画出费用图
#费用图
costmap=[0,0,0,0,0,0,0,0,0]
for c in cards:
    ct=int(c[0])
    if ct==0:#0费计到1费中
        costmap[0]+=1
        continue
    if ct > 9:#9和9费以上 者放到9中
        costmap[8]+=1
        continue
    costmap[ct-1]+=1

playname_draw.text((10,50),str(costmap),font=namefont)
    
outimg.paste(classimg,(0,0,x1,y1))
#画出卡

cardcount = 0

x_start=0
y_start=y1

for c in cards:
    #得到卡的图
    im = drawCard(c[0], c[1], c[2], c[3])
    x, y = im.size
    #画到图上
    outimg.paste(im, (x_start, cardcount * 48+y_start, x+x_start, cardcount * 48 + y+y_start))
    cardcount += 1
    if cardcount==8:#8个卡要换行一下
        x_start =256
        cardcount=0

outimg.save('out.jpg')
