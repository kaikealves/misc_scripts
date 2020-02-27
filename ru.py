#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

URL = 'https://www.prefeitura.unicamp.br/apps/site/cardapio.php' #php chamado na tabela principal
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


results = soup.find(id='sistema_cardapio') #tabela que contem cardapio completo

titulo_elems = results.find_all('span', class_='titulo_cardapio')
refeicao_elems = results.find_all('table', class_='fundo_cardapio') #cada tabela fundo_cardapio tem o cardapio do dia, mas sem titulo
titulo_elems.pop(0)

for i,job_elem in enumerate(titulo_elems):
    col = job_elem.text.strip() 
    print('-' * 80)
    print('{:^80s}'.format(col))
    print('-' * 80)
    refeicao = refeicao_elems[i] #pega apenas o almoço 
    rows = refeicao.find_all('tr')
    del rows[-1] #remove as observacoes (ultima linha da tabela)
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if ''.join(cols):
            print('{:^80s}'.format(''.join(cols)))

print('-' * 80)
