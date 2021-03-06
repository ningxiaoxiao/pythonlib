# -*- coding: UTF-8 -*-
#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import csv
import time
import json
import qrcode
import urllib
from urllib import request
from urllib import parse
import os
import shutil
from urllib.request import urlretrieve
if os.path.exists("pic") == False:
    os.mkdir("pic")
if os.path.exists("DECK") == False:
    os.mkdir("DECK")

word_css = "MSYH.TTC"


allcards = json.load(open('cards.json', encoding='utf-8'))


# 下载图片 有就跳过,没有就下载
def downloadCardImg(url, filename):
    # print(url)
    url = url.strip()
    url = url.strip('\t')
    fileurl = "pic/" + str(filename) + '.jpg'
    if os.path.exists(fileurl):  # 如果存在就不下载
        return fileurl
    urlretrieve('http:' + url, fileurl)
    return fileurl

# 把网站返回的数据转成数组


def toCardArray(jdata):
    ret = []
    tmp = {}
    for c in jdata['data']['cardID']:
        cj = findcard(c)
        # print(cj)
        # print(c)
        try:
            downloadCardImg(cj['牌组小图'], cj['url'])
        except:
            print('err url:'+cj['牌组小图'])

        if c in tmp:
            tmp[c] = [
                str(cj['cost']), cj['name'],
                int(tmp[c][2]) + 1,
                str(c)
            ]
        else:
            tmp[c] = [str(cj['cost']), cj['name'], 1, str(c)]

    for c in tmp:
        ret.append(tmp[c])
    # 按cost排序
    ret = sorted(ret, key=lambda x: int(x[0]))
    return ret

# 从全卡组中找到卡,返回详细数据


def findcard(cardid):
    for c in allcards:
        if int(c['url']) == int(cardid):
            return c


def drawCard(cost, name, count, id):
    # 先打开图片

    cardimg = Image.open('pic/' + id + '.jpg')
    cardimg = cardimg.resize((256, 48), Image.ANTIALIAS)

    cardDraw = ImageDraw.Draw(cardimg)
    # 画出cost
    costbg = Image.open('costbg.png')
    costdraw = ImageDraw.Draw(costbg)
    costfont = ImageFont.truetype(word_css, 20)
    darwTextOutline(costdraw, (7, 0), str(cost), font=costfont)
    # 把cost放到卡上
    cardimg.paste(costbg, (9, 9, 39, 39), mask=costbg)

    darwTextOutline(cardDraw, (45, 10), name,
                    ImageFont.truetype(word_css, 18), 2)
    darwTextOutline(cardDraw, (230, 9), 'x' + str(count), costfont, 2)

    return cardimg

# 从网站得数据


def getCards(code):
    data = {
        "deck_code": code,
    }
    postdata = parse.urlencode(data).encode('utf-8')
    jtext = urllib.request.urlopen("https://exp.16163.com/sv/to_cards",
                                   postdata)
    html = jtext.read().decode('utf-8')
    j = json.loads(html)
    return j  # todo 不成功的问题
# 描边


def darwTextOutline(draw, postion, text, font, size=1, color='black'):
    x, y = postion
    draw.text((x-size, y), text, font=font, fill=color)
    draw.text((x + size, y), text, font=font, fill=color)
    draw.text((x, y-size), text, font=font, fill=color)
    draw.text((x, y + size), text, font=font, fill=color)

    draw.text((x-1, y-1), text, font=font, fill=color)
    draw.text((x+1, y-1), text, font=font, fill=color)
    draw.text((x-1, y+1), text, font=font, fill=color)
    draw.text((x+1, y+1), text, font=font, fill=color)

    draw.text(postion, text, font=font)


def getdeckpic(playername, code, deck_format, mono):
    if os.path.exists("DECK/"+playername) == False:
        os.mkdir("DECK/"+playername)
    print(code)
    time.sleep(2)  # 不能太快
    bgimg = Image.open('bg.jpg')
    outimg = Image.new('RGBA', (512, 800))

    draw = ImageDraw.Draw(outimg)
    # 得到json
    cardsjson = getCards(code)
    # 转成数组
    cards = toCardArray(cardsjson)

    clan = str(cardsjson['data']['clan'])

    # 画出职业

    classimg = Image.open('class/'+clan+'.jpg')
    classimg = classimg.resize((256*2, 60*2), Image.ANTIALIAS)

    # 制出职业图的画板
    classimg_draw = ImageDraw.Draw(classimg)

    # 画出 指定/无限  无法从卡组数据中得到是指定还是无限
    # deck_format=str(cardsjson['data']['deck_format'])
    formatimg = Image.open('class/'+deck_format+'.png')
    classimg.paste(formatimg, (10, 20, 38, 48), mask=formatimg)

    # 写出名字
    namefont = ImageFont.truetype(word_css, 35)
    darwTextOutline(classimg_draw, (40, 10), playername, namefont, 2)

    # todo 画出费用图
    # 费用图
    costmap = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for c in cards:
        cost = int(c[0])
        count = int(c[2])
        if cost == 0:  # 0费计到1费中
            costmap[0] += count
            continue
        if cost > 9:  # 9和9费以上 者放到9中
            costmap[8] += count
            continue
        costmap[cost-1] += count

    plt.bar(range(len(costmap)), costmap,fc='g')
    #todo 画出柱图
    plt.savefig('1.png',transparent=True,format="png")

    darwTextOutline(classimg_draw, (10, 55), '费用:'+str(
        [1, 2, 3, 4, 5, 6, 7, 8, 9])+'\n数量:'+str(costmap), font=ImageFont.truetype(word_css, 20))
    # 把职业图放到最终上
    x1, y1 = classimg.size
    outimg.paste(classimg, (0, 0, x1, y1))
    # 画出卡
    cardcount = 0

    x_start = 0
    y_start = y1

    for c in cards:
        # 得到卡的图
        im = drawCard(c[0], c[1], c[2], c[3])
        x, y = im.size
        # 画到图上
        outimg.paste(im, (x_start, cardcount * 48+y_start,
                          x+x_start, cardcount * 48 + y+y_start))
        cardcount += 1
        if cardcount >= len(cards)/2:  # 换行一下
            x_start = 256
            cardcount = 0

    # 画出二维码

    data = "https://wiki-sv.netease.com/picker?code="+code
    qrimg = qrcode.make(data=data)
    qrimg = qrimg.resize((200, 200), Image.ANTIALIAS)
    # 算出居中位
    qrx = int(outimg.size[0]/2-qrimg.size[0]/2)
    qry = int(round((len(cards)/2+0.1)+1)*45+y_start)

    outimg.paste(qrimg, (qrx, qry, qrx+qrimg.size[0], qry+qrimg.size[1]))
    # 存出文件
    outimg.save('DECK/'+playername+'/'+playername+'_' +
                deck_format+'_'+mono+'_'+clan+'.png')


def main(jumptoindex):
    with open("2.csv", "r") as cfile:
        read = csv.reader(cfile)
        next(read)  # 跳过第一行
        count = 0
        for i in read:
            count += 1
            if count < jumptoindex:
                print("要跳到", jumptoindex, "现在是", count)
                continue
            name = i[0]
            print(str(count)+name)

            getdeckpic( name,i[2],"指定","")
            getdeckpic( name,i[3],"指定","")


            # getdeckpic( name,i[6],"_day2")
            # getdeckpic( name,i[7],"_day2")
            # getdeckpic( name,i[8],"_day2")

            # getdeckpic(name, i[2], "指定", '')
            # getdeckpic(name, i[3], "指定", '')
        print("本次比赛共计48名选手有效提交卡组 16个轮空位，请大家把群名改成卡组公示的名字，以防对手查找不到。请在明天的 16.30准备好稳定网络,推荐使用电脑端。届时会有裁判在群内公布对阵，祝大家好运~")


main(0)
# getdeckpic("ogisosetsuna","AADEPu-rbRW4uD4IJ_1J1WEqVTh7JvVGG2B7KWrWdpAOAX4","指定","")
# getdeckpic('sss',"AADEjNwjvVbupTQ1GOk69d-YU8Ea5WDVfJnXALyH0YMr5JULkY2G5eJdrtoy2RZ3-FeJ","")
