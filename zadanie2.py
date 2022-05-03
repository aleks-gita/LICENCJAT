from flask import Flask
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import random
from random import choice
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

class Zadanie2_class:
    def __init__(self):



        self.omissions = 0
        self.litery = ['A','B','C','D','E','H','I','K','L','M','O','P','R','S','T']
        self.wylosowana = None
        self.lista = []
        self.wygenerowana = []
        self.punkty = 0
        self.punkty_zle = 0
        self.liczenie = 0
        self.n = 1
        self.a = 0
        self.kolor = None
        self.kontrola =None
        self.hits = 0
        self.omissions = 0
        self.correct = 0
        self.commissions = 0
        self.wynik1 = 0
        self.wynik2 = 0
        self.wynik3 = 0

    def generowanie(self):
        litera_do_n_3=choice(self.litery)
        lista_kombinacji = []
        lista_wygenerowana1=[]
        a = 0
        i=0
        letters=self.litery
        listaA=(random.sample(letters, 5))
        lista_wolne = [elem for elem in letters if elem not in listaA]
        listaB = (random.sample(lista_wolne, 5))
        lista_wolne2 = [elem for elem in lista_wolne if elem not in listaB]
        while len(listaA) > 0:
            if self.n == 1:
                for x in listaA[i]:
                    A1 = x
                    lista_kombinacji.append(A1)
                    lista_kombinacji.append(A1)
                    break;
            if self.n == 2:
                for x in listaA[i]:
                    A1 = x
                    lista_kombinacji.append(A1)
                    for y in listaB[i]:
                        B1 = y
                        lista_kombinacji.append(B1)
                        break;
                for x in listaA[i]:
                    A1 = x
                    lista_kombinacji.append(A1)
                    break;
            if self.n == 3:
                for x in listaA[i]:
                    A1 = x
                    lista_kombinacji.append(A1)
                    for y in listaB[i]:
                        B1 = y
                        lista_kombinacji.append(B1)
                        lista_kombinacji.append(litera_do_n_3)
                        break;
                for x in listaA[i]:
                    A1 = x
                    lista_kombinacji.append(A1)
                    break;
            lista_wygenerowana1.append(lista_kombinacji)
            lista_kombinacji = []
            listaA.remove(x)
            if self.n == 2 or self.n == 3:
                listaB.remove(y)

        for i in self.litery:
            if a < (20 - 5 * self.n):
                lista_wygenerowana1.insert(random.randint(0, len(lista_wygenerowana1)), i)
                a += 1
        for i in lista_wygenerowana1:
            self.wygenerowana.extend(i)
        print(self.wygenerowana)

    def losowanie(self):

        #shuffle(self.litery)
        self.wylosowana = self.wygenerowana[self.a]
        self.lista.extend(self.wylosowana)
        print('wylosowana:', self.wylosowana)
        print('lista', self.lista)
        self.a = self.a + 1
        return self.wylosowana


    def porownanie(self, decyzja):
        wynik = None
        x = None
        index = self.wylosowana.index
        n = self.n
        if len(self.lista) > n:
            print("n", self.lista[-(n + 1)])
            for x in self.lista:
                x = str(self.lista[-(n + 1)])
        #hits
        if self.wylosowana == x and decyzja == 'TAK':
            wynik = "Dobrze"
            self.hits+=1
            self.correct+=1
            print("Znaleziono")
        if self.wylosowana != x and decyzja == 'NIE':
            wynik = "Dobrze"
            print("Dobrze")
            self.correct+=1
        #omissions
        if self.wylosowana == x and decyzja == 'NIE':
            wynik = "Zle"
            self.omissions+=1
            print("Zle")
        #commisions
        if self.wylosowana != x and decyzja == 'TAK':
            wynik = "Zle"
            self.commissions+=1
            print("Zle")
        if decyzja == "BRAK":
            wynik = "Zle"
            self.omissions += 1
            #elif self.wylosowana != x:
            #    self.commissions += 1

        if wynik == 'Dobrze':
            self.punkty += 1
            print(self.punkty)
            self.liczenie +=1
            self.kolor=1
            self.kontrola=1
        else:
            self.kolor=0
            self.punkty_zle += 1
            self.kontrola=0

    def lvl(self):
        if len(self.lista) == 25:
            self.n += 1
            self.lista=[]
            self.wygenerowana = []
            self.a = 0

    def czyszczenie(self):
        self.commissions=0
        self.omissions=0
        self.correct=0

    def obliczenie_wyniku(self):
        if self.correct>0:
            wynik = (1-((self.commissions+self.omissions)/self.correct))*100
        else: wynik = 0
        if self.n==1:
            self.wynik1=round(wynik,2)
            self.wynik = self.wynik1
        elif self.n==2:
            self.wynik2 = round(wynik, 2)
            self.wynik = self.wynik2
        elif self.n==3:
            self.wynik3 = round(wynik, 2)
            self.wynik = self.wynik3
        #self.commissions=0
        #self.omissions=0
        #self.correct=0
