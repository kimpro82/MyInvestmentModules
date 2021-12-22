# Python

- [Crawling (Naver) : Get the **Top Market Cap.** Stocks from **KOSPI** (2021.12.22)]()
- [**Numpy Financial** : **TVM** (2021.11.08)](/Python#numpy-financial--tvm-20211108)


## [Crawling (Naver) : Get the **Top Market Cap.** Stocks from **KOSPI** (2021.12.22)](/Python#python)

#### 0. Read byte stream from url
```python
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
```

#### 1.0 Read one stock's data
```python
section = soup.find('tbody')
items = section.find_all('tr', onmouseover="mouseOver(this)")[0]
# print(items)
basic_info = items.get_text()
sinfo = basic_info.split("\n")
for i in range(len(sinfo)) :
    print(i, sinfo[i])
```
> 0  
> 1 1  
> 2 삼성전자  
> 3 79,400  
> ……

#### 1.1 Read one page's data
```python
section = soup.find('tbody')
items = section.find_all('tr', onmouseover="mouseOver(this)")

for item in items :
    basic_info = item.get_text()
    sinfo = basic_info.split("\n")

    # print(sinfo[1] + '\t' + sinfo[2] + '\t' + sinfo[3] + '\t' + sinfo[15])

    if sinfo[5] != '0' :                                        # data locations are moved when the price change is 0
        list = [1, 2, 3, 15]
    else :
        list = [1, 2, 3, 11]
    length = [4, 20, 9, 9]

    for i in range(len(list)) :
        spaces = length[i]
        for char in sinfo[list[i]] :
            if char >= '가' :                                   # count 2 spaces when the letter is Korean
                spaces -= 2
            else :
                spaces -= 1
        sinfo[list[i]] += spaces * ' '

        print(sinfo[list[i]], end=' ')

    print()
```
> 1 &nbsp;&nbsp; 삼성전자&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 79,400&nbsp;&nbsp;&nbsp; 4,740,007  
> 2 &nbsp;&nbsp; SK하이닉스&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 127,000&nbsp;&nbsp; 924,563  
> 3 &nbsp;&nbsp; NAVER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 378,500&nbsp;&nbsp; 621,737  
> 4 &nbsp;&nbsp; 삼성바이오로직스&nbsp;&nbsp;&nbsp;&nbsp; 901,000&nbsp;&nbsp; 596,147  
> 5 &nbsp;&nbsp; 삼성전자우&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 71,700&nbsp;&nbsp;&nbsp; 590,010  
……

#### 1.2 Read plural pages' data
```python
pages = 2                                                       # input the last page's number

for page in range(1, pages + 1) :

    # Read data in each page
    params['page'] = page                                       # change the page number in the url
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    section = soup.find('tbody')
    items = section.find_all('tr', onmouseover="mouseOver(this)")

    # Get specific elements
    for item in items :
        basic_info = item.get_text()
        sinfo = basic_info.split("\n")

        # Set the required elements' location and their maximum size
        if sinfo[5] != '0' :                                    # data locations are moved when the price change is 0
            list = [1, 2, 3, 15]
        else :
            list = [1, 2, 3, 11]
        length = [4, 22, 9, 9]                                  # len("한국타이어앤테크놀로지") = 22

        # Print data
        for i in range(len(list)) :

            spaces = length[i]

            # Find the exact length of the text
            for char in sinfo[list[i]] :
                if char >= '가' :                               # count 2 spaces when the letter is Korean
                    spaces -= 2
                else :
                    spaces -= 1

            # Determine left or right alignment
            if sinfo[list[i]][0] < 'A' :
                sinfo[list[i]] = spaces * ' ' + sinfo[list[i]]
            else :
                sinfo[list[i]] += spaces * ' '

            # Print
            print(sinfo[list[i]], end=' ')

        print()
```
> &nbsp;&nbsp;&nbsp;1 삼성전자&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;79,400 4,740,007  
> &nbsp;&nbsp;&nbsp;2 SK하이닉스&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;127,000 &nbsp;&nbsp;924,563  
> &nbsp;&nbsp;&nbsp;3 NAVER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;378,500 &nbsp;&nbsp;621,737  
> ……  
> &nbsp;&nbsp;73 한국타이어앤테크놀로지&nbsp;&nbsp;&nbsp;&nbsp;39,850 &nbsp;&nbsp;&nbsp;49,364  
> ……  
> &nbsp;100 한솔케미칼&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;293,500 &nbsp;&nbsp;&nbsp;33,269


## [Numpy Financial : TVM (2021.11.08)](/Python#python)

- **TVM** : `PV` `FV` `FMT` `NPV` and `IRR`
- Documentation ☞ https://numpy.org/numpy-financial/latest

```python
import numpy_financial as npf

# pv(rate, nper, pmt, fv=0, when='end')
pv = npf.pv(0.1, 2, 0, 12100)
print(round(pv, 4))

# fv(rate, nper, pmt, pv, when='end')
fv = npf.fv(0.1, 2, 0, -10000)
print(round(fv, 4))

# pmt(rate, nper, pv, fv=0, when='end')
pmt = npf.pmt(0.1, 10, -10000)
print(round(pmt, 4))

# npv(rate, values)
npv = npf.npv(0.1, [-10000, +1000, +1000, +11000])
print(round(npv, 4))

# irr(values)
irr = npf.irr([-10000, 1000, 1000, 11000])
print(round(irr, 4))
```

> -10000.0  
> 12100.0  
> 1627.4539  
> -0.0  
> 0.1