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
items = section.find_all('tr', onmouseover="mouseOver(this)")[0]
# print(items)
basic_info = items.get_text()
sinfo = basic_info.split("\n")
for i in range(len(sinfo)) :
    print(i, sinfo[i])

'''
0
1 1
2 삼성전자
3 79,400
……
'''


# 2.1 Read one page's data

section = soup.find('tbody')
items = section.find_all('tr', onmouseover="mouseOver(this)")

for item in items :
    basic_info = item.get_text()
    sinfo = basic_info.split("\n")

    # print(sinfo[1] + '\t' + sinfo[2] + '\t' + sinfo[3] + '\t' + sinfo[15])

    if sinfo[5] != '0' :                                        # Data locations are moved when the price change is 0
        list = [1, 2, 3, 15]
    else :
        list = [1, 2, 3, 11]
    length = [4, 20, 10, 10]

    for i in range(len(list)) :                                 # All the ditances between neighboring columns are 20
        spaces = length[i]
        for char in sinfo[list[i]] :
            if char >= '가' :                                   # Count 2 spaces when the letter is Korean
                spaces -= 2
            else :
                spaces -= 1
        sinfo[list[i]] += spaces * ' '

        print(sinfo[list[i]], end='')

    print()

'''
1   삼성전자            79,400    4,740,007
2   SK하이닉스          127,000   924,563
3   NAVER               378,500   621,737
4   삼성바이오로직스    901,000   596,147
5   삼성전자우          71,700    590,010
……
'''