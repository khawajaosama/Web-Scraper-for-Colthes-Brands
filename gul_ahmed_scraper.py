import requests
from bs4 import BeautifulSoup
import pandas as pd
page=0
data={'product name':[],'image url':[],'product category':[]}

while(True):
    page += 1
    response =  requests.get(f'https://www.gulahmedshop.com/mens-clothes?p={page}')
    soup = BeautifulSoup(response.text,'html.parser')

    for product in soup.find_all('a', {'class':'product-item-link'}):
        
        if product.text.strip():
            
            data['product name'].append(product.text.strip())
            response2=requests.get(product.get('href'))
            
            soup2= BeautifulSoup(response2.text,'html.parser')
            
            img=soup2.find_all('img',{'itemprop':'image'})
            data['image url'].append(img[0].get('src')) if img else data['image url'].append(None)
            
            category = soup2.find_all('div',{'itemprop':'sku'})
            data['product category'].append(category[0].text) if category else data['product category'].append(None)
            
            price = soup2.find_all('span',{'class':'price'})
            data['price'].append(price[0].text) if price else data['price'].append(None)
            
    print(str(page)+' Done')
    print(len(data['product name']),len(data['image url']),len(data['product category']))
    
    if not soup.find_all('a', {'class':'action next'}):
        break
    
data = pd.DataFrame.from_dict(data)

data = pd.DataFrame.from_dict(data)
data.to_csv('gul_ahmed_data.csv')