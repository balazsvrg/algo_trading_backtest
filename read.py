
import gspread 
from tkinter import *
import pandas as pd

#a json-ön keresztül itt írom be a fájl nevét
gc = gspread.service_account(filename='finance.json')
#a google sheet kulcsát használva megnyitom és accesselem az elérést
sh = gc.open_by_key('1dEDppsJ306OLhxor_76GsV-pPLxmTt3wWhDGZjyxZe4')
#a sheet1 adatait használom
worksheet = sh.sheet1
#a sheetnek ezt a ranget használom, ezt olvasom be, külön el lehet érni sorokat, cellákat, oszlopokat vagy kiíratom az egész táblázatot
res = worksheet.get_all_records()
#printelem az egész sheetet, amit lekértem tőle

df = pd.DataFrame(res)
df = df.iloc[:342, 2:8]
df['Open'] = pd.to_numeric(df['Open'], downcast="float")
df['High'] = pd.to_numeric(df['High'], downcast="float")
df['Low'] = pd.to_numeric(df['Low'], downcast="float")
df['Close'] = pd.to_numeric(df['Close'], downcast="float")
df['Volume'] = pd.to_numeric(df['Volume'], downcast="float")
print(df.dtypes)
column = ['Date','Open', 'High', 'Low', 'Close', 'Volume']
df.to_csv('data.csv', columns=column)

