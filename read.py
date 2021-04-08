
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


def clickSetDatas():

    print(eTicker.get())
    ticker = eTicker.get()
    startDate = eStartDate.get()
    endDate = eEndDate.get()
    worksheet.update_acell('B1', ticker)
    worksheet.update_acell('B2', startDate)
    res = worksheet.update_acell('B3', endDate)


print(res)

window = Tk()
buttonTicker = Button(window, text= 'SetDatas',font=('Bahnschrift',14,'bold'),width=50,fg='#656DA7',bg='#F0F1F8')
buttonTicker.pack()
buttonTicker.config(command=clickSetDatas)
labelTicker = Label(window, text='Adj meg egy tickert:', bg = '#9F9CF7',font='Bahnschrift',fg='#F6FBED')
labelTicker.pack()
eTicker = Entry(window, bg='#C5C4F0',width=50,fg='#F6FBED', font=('Bahnschrift',12,'bold'))
eTicker.pack()
labelStartDate = Label(window, text='Adja meg a kezdő dátumot(format:éééé.hh.nn):', bg ='#9F9CF7', font='Bahnschrift' , fg = '#F6FBED')
labelStartDate.pack()
eStartDate = Entry(window, bg='#C5C4F0',width=50,fg='#F6FBED', font=('Bahnschrift',12,'bold'))
eStartDate.pack()
labelEndDate = Label(window, text='Adja meg a záró dátumot(format:éééé.hh.nn):', bg = '#9F9CF7',font='Bahnschrift',fg='#F6FBED')
labelEndDate.pack()
eEndDate = Entry(window, bg='#C5C4F0',width=50,fg='#F6FBED', font=('Bahnschrift',12,'bold'))
eEndDate.pack()
window.mainloop()