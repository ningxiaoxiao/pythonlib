import json
import csv
import urllib
from urllib import request
from urllib import parse
import os

if(not os.access("deck",os.F_OK)):
    os.mkdir("deck")
#下载图片
def downloadpng(deckcode,fname):
    if(os.access(fname,os.F_OK)):
        return
    print(fname)
    #这个只要带上token就可以了
    data={
        "token":"fb3316294fe340da92e058a53a3646cc",
        "code":deckcode
    }
    postdata=parse.urlencode(data).encode('utf-8')
    jtext=urllib.request.urlopen("https://www.iyingdi.com/verse/deck/create",postdata)
    j=json.load(jtext)
    imgurl= j["deck"]["deckImg"]
    request.urlretrieve(imgurl,filename=fname)
    


with open("Form_data.csv","r") as cfile:
    read=csv.reader(cfile)
    next(read)#跳过第一行
    for i in read:
        playerid=i[1]
        name=i[0]
        #建立文件夹
        path="deck/"+name
        if(not os.access(path,os.F_OK)):
            os.mkdir(path)
        
        downloadpng(i[3],path+"/1_day1_"+name+"_"+i[2]+".png")
        downloadpng(i[5],path+"/2_day1_"+name+"_"+i[4]+".png")
        downloadpng(i[7],path+"/3_day1_"+name+"_"+i[6]+".png")
        downloadpng(i[9],path+"/4_day1_"+name+"_"+i[8]+".png")

        downloadpng(i[11],path+"/5_day2_"+name+"_"+i[10]+".png")
        downloadpng(i[13],path+"/6_day2_"+name+"_"+i[12]+".png")
        downloadpng(i[15],path+"/7_day2_"+name+"_"+i[14]+".png")

print("d")
        