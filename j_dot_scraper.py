import requests
from bs4 import BeautifulSoup
import pandas as pd
page=0
data={'product name':[],'image url':[],'product category':[]}
while(True):
    page += 1
    response =  requests.get(f'https://www.junaidjamshed.com/mens.html?p={page}')
    soup = BeautifulSoup(response.text,'html.parser')
    
    for product in soup.find_all('a', {'class':'product-item-link'}):
        data['product name'].append(product.text.strip())
    for img_url in soup.find_all('img',{'class':'photo image'}):
        data['image url'].append(img_url.get('src'))
    
    for link in soup.find_all('a',onclick=True,href=True):
        response2 = requests.get(link.get('href'))
        soup2 = BeautifulSoup(response2.text,'html.parser')
        
        category = soup2.find_all('td',{'class':'col data'})
        if not category: data['product category'].append(None)
        else: data['product category'].append(category[-1].text)
    print(str(page)+' Done')
    if not soup.find_all('a',{'class': 'action next'}):
        break
data = pd.DataFrame.from_dict(data)

#data=data.drop_duplicates(subset='product name', keep='first')
#data=data.dropna(axis=0,how='all')
data.to_csv('data_jdot.csv')