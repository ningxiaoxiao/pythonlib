# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import json
import csv
import urllib
from urllib import request
from urllib import parse
import os
import sys
import io
FILE_DIR_ROOT = "DECK"
TOKEN = "ce97b2e644d94ffd8c699a383cf74ce5"
if (not os.access(FILE_DIR_ROOT, os.F_OK)):
    os.mkdir(FILE_DIR_ROOT)
#解决中文问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


#下载图片
def downloadpng(deckcode, playername):
    if (not os.access(FILE_DIR_ROOT + "/" + playername, os.F_OK)):
        os.mkdir(FILE_DIR_ROOT + "/" + playername)
    #这个只要带上token就可以了
    data = {"token": TOKEN, "code": deckcode}
    postdata = parse.urlencode(data).encode('utf-8')
    jtext = urllib.request.urlopen("https://www.iyingdi.com/verse/deck/create",
                                   postdata)

    j = json.load(jtext)
    if j["success"] != True:
        print("导入:" + j["msg"] + "|" + playername + "|" + deckcode)
        return

    #得到code

    deckid = j["deck"]["id"]
    #组装参数
    cards = "主牌\n"
    for i in j["cards"]["主牌"]:
        for p in j["cards"]["主牌"][i]:
            cards += p[0] + " " + p[2] + "\n"

    #更新名字和卡组名字
    data = {
        "token": TOKEN,
        "cards": cards,
        "player": playername,
        "name": playername + "_" + str(deckid),
        "id": deckid
    }
    postdata = parse.urlencode(data).encode('utf-8')

    jtext = urllib.request.urlopen("https://www.iyingdi.com/verse/deck/update",
                                   postdata)
    if j["success"] != True:
        print("修改:" + j["msg"] + "|" + playername + "|" + deckcode + "|ERR")
        return
    #组装文件名
    fname = "%s/%s/%s_%d.png" % (FILE_DIR_ROOT, playername, playername, deckid)
    j = json.load(jtext)
    #下载图片
    imgurl = j["deck"]["deckImg"]
    try:
        request.urlretrieve(imgurl, filename=fname)
    except:
        print(playername + "|" + imgurl + "|" + deckcode + "|ERR")


def main():
    with open("3withname_un.csv", "r") as cfile:
        read = csv.reader(cfile)
        next(read)  #跳过第一行
        for i in read:
            name = i[0]
            #建立文件夹
            path = FILE_DIR_ROOT + "/" + name
            if (not os.access(path, os.F_OK)):
                os.mkdir(path)

            downloadpng(i[3], name)
            downloadpng(i[5], name)


def test():
    downloadpng(
        "AADEOg8F3G9ogxfk53Ws_gKomjC7Hgp9htfGSg5qfuEEuyNsUuRtlA440h_MEo-4DX6Q",
        "ning")


downloadpng("AADExnh-oJiJmnITS0bcSQ3ykrBeFz-kTiD4STKU1dEPFdFvm3z-J7K98Mqe1JhrR55S","克里斯丁娜")
