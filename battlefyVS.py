# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import json
import csv
import urllib
from urllib import request

url = 'https://api.battlefy.com/stages/5badda4416831f03b7235206/matches?roundNumber=5'

resData = urllib.request.urlopen(url)

j = json.loads(resData.read().decode('utf-8-sig'))

xls = open('vs.csv', 'w', encoding='gbk')
cw = csv.writer(xls)
cw.writerow(['name1', 'points1', 'points2', 'name2'])

count = 0
name1 = ''
p1 = ''
p2 = ''
name2 = ''

for m in j:
    count += 1
    name1 += m['top']['team']['name'] + '\r\n'
    name2 += m['bottom']['team']['name'] + '\r\n'

    p1 += str(m['top'].get('score', 0)) + '\r\n'

    p2 += str(m['bottom'].get('score', 0)) + '\r\n'

    print(m['top']['team']['name'], m['top'].get('score', 0), m['bottom'].get(
        'score', 0), m['bottom']['team']['name'])

    if count == 6:
        cw.writerow([name1, p1, p2, name2])
        count = 0
        name1 = name2 = p1 = p2 = ''

print('ojbk')
