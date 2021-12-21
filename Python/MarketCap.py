import requests
from bs4 import BeautifulSoup


# 1. Read byte stream from url

url = 'https://finance.naver.com/sise/sise_market_sum.naver'
params = {
    'sosok' : '0',                                              # 1 : KOSPI, 2 : KOSDAQ
    'page' : '1',
}

response = requests.get(url, params=params)
# print(response)                                               # <Response [200]>
# print(type(response))                                         # <class 'requests.models.Response'>
# print(response.content)                                       # byte stream (encoded) : b'\n\n\n\n\n\n\n<!--
# print(type(response.content))                                 # <class 'bytes'>

soup = BeautifulSoup(response.content, "html.parser")
# print(soup)
# print(type(soup))                                             # <class 'bs4.BeautifulSoup'>


# 2.0 Read one stock's data

section = soup.find('tbody')
items = section.find_all('tr', onmouseover="mouseOver(this)")[8]
# print(items)
basic_info = items.get_text()
sinfo = basic_info.split("\n")
for i in range(len(sinfo)) :
    print(i, sinfo[i])

'''
0
1 1
2 삼성전자
3 78,100
……
'''


# 2.1 Read one page's data

section = soup.find('tbody')
items = section.find_all('tr', onmouseover="mouseOver(this)")

for item in items :
    basic_info = item.get_text()
    sinfo = basic_info.split("\n")

    if sinfo[5] != '0' :                                        # Data locations are moved when the price change is 0
        list = [1, 2, 3, 15]
    else :
        list = [1, 2, 3, 11]

    for i in list :                                             # All the ditances between neighboring columns are 20
        length = 20
        for char in sinfo[i] :
            if char >= '가' :                                   # Count 2 spaces when the letter is Korean
                length -= 2
            else :
                length -= 1
        sinfo[i] += length * ' '

        print(sinfo[i], end='')

    print()

'''
1                   삼성전자            78,100              4,662,400
2                   SK하이닉스          124,500             906,363
3                   NAVER               375,000             615,988
4                   삼성바이오로직스    929,000             614,673
5                   삼성전자우          71,000              584,250
……
'''