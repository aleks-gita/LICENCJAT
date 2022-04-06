import ast
from random import choice


class Zadanie3:
    def __init__(self):
        self.list_of_lists = [
            [6, 2, 9],
            [4, 1, 5],
            [3, 2, 7, 9],
            [1, 9, 6, 8],
            [1, 5, 2, 8, 6],
            [6, 1, 8, 4, 3],
            [5, 3, 9, 4, 1, 8],
            [7, 2, 4, 8, 5, 6],
            [8, 1, 2, 9, 3, 6, 5],
            [4, 7, 3, 9, 1, 2, 8],
            [9, 4, 3, 7, 6, 2, 5, 6],
            [7, 2, 8, 1, 9, 6, 5, 2]]
        self.dlugosc = 3
        self.wylosowana = None

    def losowanie(self):
        listy_aktualne = []
        for x in self.list_of_lists:
            if len(x) == self.dlugosc:
                listy_aktualne.append(x)

        self.wylosowana = choice(listy_aktualne)
        return self.wylosowana
        #print(listy_aktualne)
        # if len(self.lista) == self.dlugosc:

    def sprawdzenie(self, lista):
        backward = list(reversed(self.wylosowana))

        new_list = ''.join(str(lista).split(','))
        new_list = list(new_list)
        dd = [ast.literal_eval(i) for i in new_list]

        print("backward", backward)
        print("Uzytkownik", dd)

        if dd == backward:
            print("dobrze")
            self.dlugosc +=1
        else:
            print("zle")



