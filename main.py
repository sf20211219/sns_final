import pandas as pd
import requests
from bs4 import BeautifulSoup

## 마지막 페이지 수 구하기
url = "https://www.yes24.com/product/category/bestseller?categoryNumber=001&pageNumber=1&pageSize=24"
res = requests.get(url)
html = res.text

soup = BeautifulSoup(html, "lxml")
target = soup.select('a.bgYUI.end')

end_page = int(target[0].get('title'))

## 크롤링
bestList = []

for page_num in range(1, end_page + 1):
    p_url = f"https://www.yes24.com/product/category/bestseller?categoryNumber=001&pageNumber={page_num}&pageSize=24"
    p_res = requests.get(p_url)
    p_html = p_res.text

    p_soup = BeautifulSoup(p_html, "lxml")
    p_target = p_soup.select('div.itemUnit')

    for item in p_target:
        rank = item.select('em.ico.rank')[0].text
        title = item.select('a.gd_name')[0].text
        writer = (item.select('span.authPub.info_auth a') or item.select('span.authPub.info_auth'))[0].text.strip()
        publisher = item.select('span.authPub.info_pub a')[0].text
        date = item.select('span.authPub.info_date')[0].text

        bestList.append([rank, title, writer, publisher, date])

## csv 저장
df = pd.DataFrame(bestList, columns=['순위', '제목', '저자', '출판사', '출판월'])
df.to_csv('bestseller_list.csv', index=False, encoding='utf-8')