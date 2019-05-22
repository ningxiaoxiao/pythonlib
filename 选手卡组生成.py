# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from selenium import  webdriver
from selenium.webdriver.chrome.options import Options
import csv
import os,shutil
from urllib.request import urlretrieve
if os.path.exists("C:/deckshare/pic") ==False:
    os.mkdir("C:/deckshare/pic")
from PIL import Image, ImageDraw, ImageFont





word_css  = "DFHeiW7.ttf" 
font = ImageFont.truetype(word_css,20)
costfont = ImageFont.truetype(word_css,30)

outimg=Image.open('bg.jpg')
draw=ImageDraw.Draw(outimg)
cards=[]
def urllib_download(url,filename):
    print(url)
    fileurl="C:/deckshare/pic/"+filename+'.jpg'
    if os.path.exists(fileurl):#如果存在就不下载
        return fileurl
    urlretrieve(url, fileurl)
    return fileurl  
def downloaddeck(code):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://wiki-sv.netease.com/picker?specify=false&code='+code)
    pickedlist=driver.find_elements_by_class_name('m-picked-card')


    for card in pickedlist:
        name=card.find_element_by_class_name('name').text.replace('‧',' ')
        cost=card.find_element_by_class_name('cost').text
        count=card.find_element_by_class_name('quantity').text.replace('×','')
        cardid=card.find_element_by_class_name('remove').get_attribute('data-card-id')

        picurl=card.get_attribute('style')
        picurl=picurl.replace('");','').replace('background-image: url("','http:')
            
        pic=urllib_download(picurl,cardid)
        cards.append([cost,name,count,cardid])

    driver.quit()

def drawCard(cost,name,count,id):
    #先打开图片
    
    cardimg=Image.open('pic/'+id+'.jpg')
    cardimg=cardimg.resize((256,48),Image.ANTIALIAS)


    cardDraw =ImageDraw.Draw(cardimg)
    #cost
    costbg=Image.open('costbg.png')
    
    costdraw=ImageDraw.Draw(costbg)
    costdraw.text((7,0),cost,font=costfont)
    cardimg.paste(costbg,(9,9,39,39))

    
    cardDraw.text((39,12),name,font=font)
    cardDraw.text((220,9),'x'+count,font=costfont)
    #cardimg.show()
    return cardimg
downloaddeck('AADEzjgLLyqmHQD_e-be9FiMFu8TMG7od98U1Vwfp4MJAuj-cGml2cH_gPl0w4Fm9loP')
cards=sorted(cards,key=lambda x:x[0])
#todo 画出职业 和指定/无限
#todo 画出费用图
cardcount=0
for c in cards:
    #得到卡的图
    im=drawCard(c[0],c[1],c[2],c[3])
    x, y = im.size
    #画到图上
    outimg.paste(im,(0,cardcount*48,x,cardcount*48+y))
    cardcount+=1
outimg.show()

