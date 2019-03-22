# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import json
import csv
import urllib
from urllib import request

url = 'https://dtmwra1jsgyb0.cloudfront.net/stages/5badda4416831f03b7235206/rounds/5/standings'

resData = urllib.request.urlopen(url)
j = json.loads(resData.read().decode('utf-8'))

rank = 0

xls = open('points.csv', 'w', encoding='gbk')
cw = csv.writer(xls)
cw.writerow([
    'name', 'W-L', 'points', 'opponentsMatchWinPercentage', 'gameWinPercentage'
])

count = 0
allname = ''
allwl = ''
allpoints = ''
allomp = ''
allgwp = ''

for m in j:
    rank += 1
    count += 1

    allname += m['team']['name'] + '\r\n'
    allwl += str(m['wins']) + ' - ' + str(m['losses']) + '\r\n'
    allpoints += str(m['points'] / 3) + '\r\n'
    allomp += str(round(m['opponentsMatchWinPercentage'], 2)) + '\r\n'
    allgwp += str(round(m['gameWinPercentage'], 2)) + '\r\n'

    print(m['team']['name'])

    # 先手收集 12名 写入一行
    if count == 12:
        cw.writerow([allname, allwl, allpoints, allomp, allgwp])
        count = 0
        allname = ''
        allwl = ''
        allpoints = ''
        allomp = ''
        allgwp = ''

print('ojbk')
