#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys
import datetime

#TODO: day input (https://www.prefeitura.unicamp.br/apps/site/cardapio.php?d=2020-03-06)

_ALLOWED_ARGS = ['-o', '-d']
_ALLOWED_OPT = ['NOFORMAT']
URL = 'https://www.prefeitura.unicamp.br/apps/site/cardapio.php' #php chamado na tabela principal

if len(sys.argv) % 2 == 0:
    raise ValueError('Wrong input')

format_en = False 
day = None 

for idx in range(1, len(sys.argv), 2):
    if sys.argv[idx] not in _ALLOWED_ARGS:
        raise ValueError('Invalid arg')
    if str(sys.argv[idx]) == "-o":
        if sys.argv[idx + 1] not in _ALLOWED_OPT:
            raise ValueError('wrong option')
        if str(sys.argv[idx + 1]) == "NOFORMAT":
            format_en = True 
    elif str(sys.argv[idx]) == "-d":
        day = str(sys.argv[idx + 1])
        datetime.datetime.strptime(day, '%Y-%m-%d')

if day:
    URL = URL + "?d=" + str(day)

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='sistema_cardapio') #tabela que contem cardapio completo

calendario_elems = results.find_all('p', class_='titulo')
titulo_elems = results.find_all('span', class_='titulo_cardapio')
if(len(titulo_elems) == 0):
    raise ValueError('Cardápio não disponível para o dia ' + str(day))
refeicao_elems = results.find_all('table', class_='fundo_cardapio') #cada tabela fundo_cardapio tem o cardapio do dia, mas sem titulo
titulo_elems.pop(0)


print('-' * 80)

for calendario_elem in calendario_elems:
    col = calendario_elem.text.strip()
    str1, str2 = col.split('-', 1)
    if not format_en:
        print('{:^80s}'.format(str1.strip()).title())
        print('{:^80s}'.format(str2.strip()))
    else:
        print(str1.strip())
        print(str2.strip())


for i,job_elem in enumerate(titulo_elems):
    col = job_elem.text.strip() 
    if not format_en:
        print('-' * 80)
        print('{:^80s}'.format(col))
        print('-' * 80)
    else:
        print(col)
    refeicao = refeicao_elems[i] 
    rows = refeicao.find_all('tr')
    del rows[-1] #remove as observacoes (ultima linha da tabela)
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if ''.join(cols):
            n = 70
            if not format_en:
                line = ''.join(cols)
                [print('{:^80s}'.format(line[i:i+n]).title()) for i in range(0, len(line), n)]
            else:
                print(''.join(cols))

print('-' * 80)
