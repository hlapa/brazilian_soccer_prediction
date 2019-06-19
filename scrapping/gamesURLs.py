# Imports bibliotecas plus configuração webdriver
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
import time
import random
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("error")
options = webdriver.ChromeOptions()
options.add_argument("--headless")


def url_ano(ano):
    if ano == 2017:
        temp='13464/all-games'
        temp2='13464/all-games/page/2'
    elif ano== 2018:
        temp= '15366/all-games'
        temp2='15366/all-games/page/2'
    elif ano==2016:
        temp='12284/all-games'
        temp2='12284/all-games/page/2'
    elif ano==2015:
        temp='11185/all-games'
        temp2='11185/all-games/page/2'
    elif ano==2014:
        temp='9097/all-games'
        temp2='9097/all-games/page/2'
    elif ano==2013:
        temp='7971/all-games'
        temp2='7971/all-games/page/2'
    elif ano==2012:
        temp='6826/all-games'
        temp2='6826/all-games/page/2'
    elif ano==2011:
        temp='5830/all-games'
        temp2='5830/all-games/page/2'
    elif ano==2010:
        temp='4996/all-games'
        temp2='4996/all-games/page/2'
    elif ano==2009:
        temp='3220/all-games'
        temp2='3220/all-games/page/2'
    elif ano==2008:
        temp='2598/all-games'
        temp2='2598/all-games/page/2'
    elif ano==2007:
        temp='1965/all-games'
        temp2='1965/all-games/page/2'
        
    return temp, temp2



resultados=[]
datas=[]
time_casa=[]
time_visitante=[]
ids=[]
links=[]
for ano in range(2007,2019):
    print('Estou no ano: ',ano)
    url_page_1,url_page_2=url_ano(ano)
    url='https://www.academiadasapostasbrasil.com/stats/competition/brasil-stats/26/'
    url=url+url_page_1
    url2=url+url_page_2
    driver= webdriver.Chrome(r'chromedriver',options=options)
    driver2= webdriver.Chrome(r'chromedriver',options=options)
    driver.get(url)
    time.sleep(random.randint(2,4))
    driver2.get(url2)
    page_source=driver.page_source
    page_source2=driver2.page_source
    parsed_content = BeautifulSoup(page_source, 'html.parser')
    parsed_content2=BeautifulSoup(page_source2, 'html.parser')
    tabela=parsed_content.tbody
    tabela2=parsed_content2.tbody
    tamanho=len(tabela.find_all('span',{'class':'icon-aa aa-icon-player active'}))
    tamanho2=len(tabela2.find_all('span',{'class':'icon-aa aa-icon-player active'}))

    contador=0
    for n in range(tamanho):
        resultado=tabela.find_all('td',{'class':'darker'})[contador].text.strip()
        resultados.append(resultado)
        data=tabela.find_all('td',{'class':'darker tipsy-active nowrap'})[contador].get("original-title")
        datas.append(data)
        contador+=1
        print('Estou no jogo: ',contador)

    contador=0
    flag=0
    for n in range(tamanho*2):
        if flag % 2 == 0:
                time_a=tabela.find_all('a',{'class':''})[contador].text
                time_casa.append(time_a)
        else:
                time_b=tabela.find_all('a',{'class':''})[contador].text
                time_visitante.append(time_b)
        
        contador+=2
        flag+=1


    contador=0
    for n in range(tamanho2):
        resultado=tabela2.find_all('td',{'class':'darker'})[contador].text.strip()
        resultados.append(resultado)
        data=tabela2.find_all('td',{'class':'darker tipsy-active nowrap'})[contador].get("original-title")
        datas.append(data)
        contador+=1

    contador=0
    flag=0
    for n in range(tamanho2*2):
        if flag % 2 == 0:
                time_a=tabela2.find_all('a',{'class':''})[contador].text
                time_casa.append(time_a)
        else:
                time_b=tabela2.find_all('a',{'class':''})[contador].text
                time_visitante.append(time_b)
        contador+=2
        flag+=1

    contador=0
    for n in range(tamanho):
        rg_partida=tabela.find_all('tr',id)[1].get("id")
        ids.append(rg_partida)
        link=tabela.find_all('span',{'class':'icon-aa aa-icon-player active'})[contador].find_parent().get("href")
        links.append(link)
        contador+=1    

    contador=0
    for n in range(tamanho2):
        rg_partida=tabela2.find_all('tr',id)[1].get("id")
        ids.append(rg_partida)
        link=tabela2.find_all('span',{'class':'icon-aa aa-icon-player active'})[contador].find_parent().get("href")
        links.append(link)
        contador+=1  

df=pd.DataFrame({'data':datas,
                 'time_casa':time_casa,
                 'time_visitante':time_visitante,
                 'resultado':resultados,
                 'id_partida':ids,
                 'link':links})

df.to_csv('gamesDB.csv')