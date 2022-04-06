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

Session = sessionmaker(bind = engine)
session = Session()




class Zadanie2:
    def __init__(self):
        self.litery = ['F', 'H', 'J', 'K', 'L', 'N']# 'P', 'Q', 'R']  # , 'S', 'T', 'Y']
        self.wylosowana = None
        self.lista = []
        self.punkty = 0
        self.liczenie = 0
        self.n=1

    def losowanie(self):
        shuffle(self.litery)
        self.wylosowana = choice(self.litery)
        self.lista.extend(self.wylosowana)
        print('wylosowana:', self.wylosowana)
        print('lista', self.lista)
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

        if self.wylosowana == x and decyzja == 'TAK':
            wynik = "Dobrze"
            print("Znaleziono")
        if self.wylosowana != x and decyzja == 'NIE':
            wynik = "Dobrze"
            print("Dobrze")
        if self.wylosowana == x and decyzja == 'NIE':
            wynik = "Zle"
            print("Zle")
        if self.wylosowana != x and decyzja == 'TAK':
            wynik = "Zle"
            print("Zle")

        if wynik == 'Dobrze':
            self.punkty += 1
            print(self.punkty)
            self.liczenie +=1
    def lvl(self):
        if self.liczenie == 5:
            self.n += 1
            self.liczenie = 0
