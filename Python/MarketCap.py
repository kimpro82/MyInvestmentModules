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

# section = soup.find('tbody')
# items = section.find_all('tr', onmouseover="mouseOver(this)")[0]
# # print(items)
# basic_info = items.get_text()
# sinfo = basic_info.split("\n")
# for i in range(len(sinfo)) :
#     print(i, sinfo[i])


# 2.1 Read one page's data

section = soup.find('tbody')
items = section.find_all('tr', onmouseover="mouseOver(this)")
for item in items :
    basic_info = item.get_text()
    sinfo = basic_info.split("\n")
    # sinfo[2] += int((20 - len(sinfo[2])) / 8) * '\t'
    for i in [1, 2, 3, 15] :
        print(sinfo[i], end='\t')
    print()