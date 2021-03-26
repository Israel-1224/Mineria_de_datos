import requests
import io
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from typing import Tuple, List
import re
from datetime import datetime

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_csv_from_url(url:str) -> pd.DataFrame:
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')))

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))



def wiki() -> pd.DataFrame:
    soup = get_soup("https://es.wikipedia.org/wiki/Anexo:Los_100_mejores_libros_de_todos_los_tiempos,_seg%C3%BAn_el_Club_de_Libros_de_Noruega")
    list_of_lists = [] # :List
    rows = soup.table.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        #  listado_de_valores_en_columnas = []
        #  for column in columns:
        #    listado_de_valores_en_columnas.append(coulmn.text.strip())
        listado_de_valores_en_columnas = [column.text.strip() for column in columns]
        list_of_lists.append(listado_de_valores_en_columnas)

    return pd.DataFrame(list_of_lists, columns=[header.text.strip() for header in  rows[0].find_all('th')])


df = wiki()
print_tabulate(df)
df.to_csv("csv/estados.csv", index=False)

def remove_repeated_number(str_repeated_value:str)->float:
    if(type(str_repeated_value)!=str):
        str_repeated_value = str(str_repeated_value)
    str_sin_0 = re.sub("^0+", '', str_repeated_value)
    str_sin_comma = str_sin_0.replace(',','')
    num = 0.0
    if len(str_sin_comma) % 2 == 0:
        mitad = int(len(str_sin_comma)/2)
        num = float(str_sin_comma[0:mitad])
    return num

def remove_repeated_date(str_date_repeated:str) -> datetime:
    return datetime.strptime(str_date_repeated[0:8],'%Y%m%d')


