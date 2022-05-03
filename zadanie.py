
from flask import Flask
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import random
from random import random
from random import choice
from random import randrange
from random import shuffle

engine = create_engine('sqlite:///./Lic.db', connect_args={'check_same_thread': False})

META_DATA = MetaData(bind=engine)

c = engine.connect()
META_DATA.reflect()

# select kart z tabel
baza_dzialan = META_DATA.tables['LIC']
punkty_zad1= META_DATA.tables['Punkty_zad1']

Session = sessionmaker(bind = engine)
session = Session()

dzialania_select = baza_dzialan.select()
c=engine.execute(dzialania_select)
result= c.fetchall()

class Zadanie:
    def __init__(self):
        self.litery=['F', 'H', 'J', 'K', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'Y']
        self.litery_wylosowane =[]
        self.zurzyte=[]
        self.wylosowne = []
        self.dzialania=[i[0] for i in result]
        self.wywolane = []
        self.lista_uzytkownik = {}
        self.wybrana= None
        self.wyswitlane = 0
        self.rezultat = 0
        self.punkty = 0
        self.dobrze = 0
        self.zle =0
        self.wszystkie_litery = 0
        self.dobrze_statystyka = 0
        self.zle_statystyka = 0
        self.procenty= 0
        self.dlugosc_bloku=0
        self.punkty_do_statystyki = 0
        self.wszystkie_do_statystyki =0
        #self.wylosuj()
        #self.wynik()
    def losuj_dlugosc_bloku(self):
        #lista_dl=[3,4,5,6,7]
        self.dlugosc_bloku = choice(range(3,7))
        print("dlugosc_bloku", self.dlugosc_bloku)
        return self.dlugosc_bloku
    def pomieszanie(self):
        shuffle(self.dzialania)
    def wylosuj(self):
        if len(self.dzialania) == 1:
            self.przeladowanie()
            wylosowane = self.dzialania[19]  # zapelnienie luki - 19 jest losowe
            self.wylosowne.append(wylosowane)
        else:
            wylosowane = self.dzialania[0]#randrange(1, len(self.dzialania))
            self.wylosowne.append(wylosowane)
            self.wywolane.append(wylosowane)
            #print(wylosowane)
            #print(self.wylosowne)
            x= self.dzialania.index(wylosowane)
            del self.dzialania[x]
            #print(self.dzialania)
            #print(len(self.dzialania))

    def przeladowanie(self):
        shuffle(self.wywolane)
        self.dzialania.extend(self.wywolane[:])
        del self.wywolane[:]

    def wyswietl(self):
        qur = session.query(baza_dzialan).filter(baza_dzialan.c.ID.in_(self.wylosowne)).all()
        dzialania_baza = ([i.Dzialanie for i in qur])
        print("DZIAALNIE", str(dzialania_baza))
        print(*dzialania_baza, sep =', ')
        return dzialania_baza

    def czyszczenie(self):
        self.wylosowne = []

    def wynik(self):
        #print("WYTLOSOWNAE",self.wylosuj)
        qur = session.query(baza_dzialan).filter(baza_dzialan.c.ID.in_(self.wylosowne)).all()
        wynik_prawda = ([i.Dobry for i in qur])
        wynik_falsz = ([i.Zly for i in qur])
        falsz = 0
        prawda = 0
        for x in wynik_falsz:
            falsz = x
        for x in wynik_prawda:
            prawda = x
        print('falsz', falsz)
        print('prawda', prawda)
        L= [wynik_prawda, wynik_falsz]
        self.wyswitlane = choice(L)
        return self.wyswitlane

    def sprawdzenie(self, status):
        qur = session.query(baza_dzialan).filter(baza_dzialan.c.ID.in_(self.wylosowne)).all()
        wynik_prawda = ([i.Dobry for i in qur])
        wynik_falsz = ([i.Zly for i in qur])
        y = 0
        x = 0
        print("Wylosowana", self.wylosowne)
        print("Liczba", self.wyswitlane)
        print("Prawda", wynik_prawda)
        if self.wyswitlane == wynik_prawda:
            y = 1
        if status == "Prawda":
            x = 1
        if y == x:
            print("Zgadza sie")
            self.dobrze += 1
            self.dobrze_statystyka += 1
        else:
            print("Nie zgadza sie")
            self.zle += 1
            self.zle_statystyka += 1

        #if self.wyswitlane == wynik_falsz and status == "Falsz":
        #    x = 1
        #    y = 1
        #    print("Zgadza sie")
        #else:
       #     print("Nie zgadza sie")

        print("FFFFFFFf", status)
        print("y:", y)
        print('x', x)


    def rezultat(self):
        qur = session.query(baza_dzialan).filter(baza_dzialan.c.ID.in_(self.wylosowne)).all()
        wynik_prawda = ([i.Dobry for i in qur])
        wynik_falsz = ([i.Zly for i in qur])

        if self.wyswitlane == wynik_prawda:
            self.rezultat = 1
        else:
            self.rezultat = 0
        print("rezultat", self.rezultat)
        return self.rezultat

    def litery_los(self):
        self.wybrana = choice(self.litery)
        self.litery_wylosowane.append(self.wybrana)
        x = self.litery.index(self.wybrana)
        del self.litery[x]
        return self.wybrana

    def lista(self, index, value):
        self.lista_uzytkownik = {**self.lista_uzytkownik, **{value: index}}
        #self.lista_uzytkownik.insert(index - 1, value)
        print(self.lista_uzytkownik)

    def litery_sprawdzenie(self):
        lista_key = list(self.lista_uzytkownik.keys())
        punkty = 0
        for x in self.litery_wylosowane:
            if x in lista_key:
                print('JEST', self.lista_uzytkownik[x])
                print(x, self.litery_wylosowane.index(x))
                if self.lista_uzytkownik[x]  == self.litery_wylosowane.index(x):
                    punkty += 1
        self.wszystkie_litery = len(self.litery_wylosowane)
        self.punkty = punkty
        print('Punkty',self.punkty , '/', self.wszystkie_litery)

    def czyszczenie_tabela(self):
        self.litery.extend(self.litery_wylosowane[:])
        del self.litery_wylosowane[:]

    def wyzerowanie_odp(self):
        self.dobrze = 0
        self.zle = 0

    def procent(self):
        self.procenty= (self.dobrze / (self.dobrze + self.zle)) * 100
        self.procenty = int(self.procenty)

    def statystyka(self):
        if self.punkty == self.wszystkie_litery:
            self.punkty_do_statystyki += self.punkty
            self.wszystkie_do_statystyki += self.wszystkie_litery
        else:
            self.punkty_do_statystyki += 0
            self.wszystkie_do_statystyki += self.wszystkie_litery
        print("Punkty statystyka", self.punkty_do_statystyki)










