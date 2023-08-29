import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

url = ('https://listado.mercadolibre.com.ar/cervezas#D[A:cervezas]')


response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
   # h2[@class="ui-search-item__title shops__item-title"]
   
    productos = soup.find_all('h2',attrs={'class':'ui-search-item__title'})

    productos = [i.text for i in productos]
    
    # Todos los titulos : print(productos)
    
    urls = soup.find_all('a', attrs={'class','ui-search-item__group__element shops__items-group-details ui-search-link'})
    
    urls = [i.get('href') for i in urls]
    
    #Todas las url: print(urls)
    
    dom = etree.HTML(str(soup))
    precios = dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-columns shops__content-columns"]/div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div//div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="andes-money-amount__fraction"]')
    
    precios = [i.text for i in precios]
    
    #Todos los precios: print(precios)
    
    #df = pd.DataFrame({'titulo':productos, 'url': urls, 'precios':precios})
    
    #print(df)
    
    #df.to_csv('cervezas_mercado_libre.csv')
    
    #//div[@class="ui-search-pagination shops__pagination-content"]/ul/li[contains(@class,"--next")]/a
    
    siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]/nav/li[contains(@class,"--next")]/a')[0].get('href')
    
    #print(siguiente)
    
    #//span[@class="andes-pagination__link"]
    ini = soup.find('span', attrs={"class": "andes-pagination__link"}).text
    ini = int(ini)
    #print(ini)
    
    #//li[@class="andes-pagination__page-count"]
    can = soup.find('li', attrs= {"class": "andes-pagination__page-count"})
    can = int(can.text.split(" ")[1])
    #print(can)
    
    lista_titulos = []
    lista_url = []
    lista_precios = []
    
    siguiente = url
    while True:
        r = requests.get(siguiente)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content,'html.parser')
            #Titulos
            productos = soup.find_all('h2',attrs={'class':'ui-search-item__title'})
            productos = [i.text for i in productos]
            lista_titulos.extend(productos)
            #Url
            urls = soup.find_all('a', attrs={'class','ui-search-item__group__element shops__items-group-details ui-search-link'})
            urls = [i.get('href') for i in urls]
            lista_url.extend(urls)
            #Precios
            dom = etree.HTML(str(soup))
            precios = dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-columns shops__content-columns"]/div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div//div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="andes-money-amount__fraction"]')           
            precios = [i.text for i in precios]
            lista_precios.extend(precios)
            
            ini = soup.find('span', attrs={"class": "andes-pagination__link"}).text
            ini = int(ini)
            can = soup.find('li', attrs= {"class": "andes-pagination__page-count"})
            can = int(can.text.split(" ")[1])
            
        else:
            break
        print(ini, can)
        if ini == can:
            break
        siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]/nav/li[contains(@class,"--next")]/a')[0].get('href')
        
    df = pd.DataFrame({"titulo":lista_titulos,"url":lista_url,"precio":lista_precios})
    print (df)