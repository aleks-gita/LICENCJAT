
from flask import Flask
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from random import random
from random import randrange
from random import shuffle

engine = create_engine('sqlite:///./Lic.db', connect_args={'check_same_thread': False})

META_DATA = MetaData(bind=engine)

c = engine.connect()
META_DATA.reflect()

# select kart z tabel
baza_dzialan = META_DATA.tables['LIC']

Session = sessionmaker(bind = engine)
session = Session()

dzialania_select = baza_dzialan.select()
c=engine.execute(dzialania_select)
result= c.fetchall()

class Zadanie:
    def __init__(self):
        self.litery=['F', 'H', 'J', 'K', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'Y']
        self.zurzyte=[]
        self.wylosowne = []
        self.dzialania=[i[0] for i in result]
        self.wywolane = []
        self.wylosuj()

    def wylosuj(self):
        if len(self.dzialania) == 1:
            self.przeladowanie()
            wylosowane = self.dzialania[19]  # zapelnienie luki - 19 jest losowe
            self.wylosowne.append(wylosowane)
        else:
            wylosowane = self.dzialania[0]#randrange(1, len(self.dzialania))
            self.wylosowne.append(wylosowane)
            self.wywolane.append(wylosowane)
            print(wylosowane)
            print(self.wylosowne)
            #return wylosowane
            x= self.dzialania.index(wylosowane)
            del self.dzialania[x]
            print(self.dzialania)
            print(len(self.dzialania))

    def przeladowanie(self):
        shuffle(self.wywolane)
        self.dzialania.extend(self.wywolane[:])
        del self.wywolane[:]

    def wyswietl(self):
        qur = session.query(baza_dzialan).filter(baza_dzialan.c.ID.in_(self.wylosowne)).all()
        dzialania_baza = ([i.Dzialanie for i in qur])

        # Printing list using sep Method
        #print(*ini_list, sep=', ')
        print("DZIAALNIE", str(dzialania_baza))
        print(*dzialania_baza, sep =', ')
        #self.wynik()
        return dzialania_baza
    
    def wynik(self):
        qur = session.query(baza_dzialan).filter(baza_dzialan.c.ID.in_(self.wylosowne)).all()
        wynik_prawda = ([i.Dobry for i in qur])
        wynik_falsz = ([i.Zly for i in qur])
        self.wylosowne = []
        return wynik_prawda, wynik_falsz


