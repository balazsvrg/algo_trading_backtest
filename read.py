
import gspread 
from tkinter import *

#a json-ön keresztül itt írom be a fájl nevét
gc = gspread.service_account(filename='finance.json')
#a google sheet kulcsát használva megnyitom és accesselem az elérést
sh = gc.open_by_key('1dEDppsJ306OLhxor_76GsV-pPLxmTt3wWhDGZjyxZe4')
#a sheet1 adatait használom
worksheet = sh.sheet1
#a sheetnek ezt a ranget használom, ezt olvasom be, külön el lehet érni sorokat, cellákat, oszlopokat vagy kiíratom az egész táblázatot
res = worksheet.get_all_records()
#printelem az egész sheetet, amit lekértem tőle
print(res)


