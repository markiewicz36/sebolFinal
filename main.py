#####################################
# Program wypożyczalnia aut
# Pozwala na dowolne dodawanie, usuwanie klentów oraz samochdów
# Pozwala wypożyczyć (przypisać samochód) do kontkretnego klienta
# Każdy klient ma swoje saldo które można doładować
# Każde wypożyczenie kosztuje, jeśli klient nie ma wystarczającej ilości środków takie wypożyczenie chuj strzeli
#
#Stworzenie klasy Baza - odpowiedzialna za przetrzymywanie wszystkich informacji o klientach oraz pojazdach
class Baza:

    #Stworzenie list
    listaSamochodow = []
    listaKlientow = []
    samochodyWypozyczone = []

    #Konstruktor klasy
    def __init__(self):
        self.listaKlientow = []
        self.listaSamochodow = []
        self.samochodyWypozyczone = []

    #Funkcja odpowiedzialna za wyświetlanie wszystkich klientów wraz z informacjami
    def wyswietlListeKlientow(self):
        index = 1
        for x in self.listaKlientow:
            print(index,'-',x.informacjeKlient())
            index += 1

    #Funkcja odpowiedzialna za wyświetlanie wszystkich samochodów wraz z informacjami
    def wyswietlListeSamochodow(self):
        index = 1
        for x in self.listaSamochodow:
            print(index,x.informacjeSamochod())
            index += 1

    #Funkcja odpowiedzialna za wyświetlanie wszystkich samochodów wypożyczonych wraz z informacjami
    def wyswietlListeSamochodowWypozyczonych(self):
        index = 1
        for x in self.samochodyWypozyczone:
            print(index,x.informacjeSamochod())
            index += 1

    #Funkcja dodająca klienta do bazy
    def dodajKlienta(self):
        imie = input('Imie: ')
        nazwisko = input('Nazwisko: ')
        wiek = input('Wiek: ')
        try:
            self.listaKlientow.append(Klient(imie, nazwisko, wiek))
            print('Dodano klienta!')
        except ValueError:
            print('Błąd przy dodawaniu klienta!')

    #Funkcja usuwająca klienta z bazy (wypożyczone samochody zostają przywrócone do listy dostępnych samochodów)
    def usunKlienta(self):
        print('Wybierz którego klienta chcesz usunąć: ')
        self.wyswietlListeKlientow()
        wyobr = int(input('Wybór: '))
        for x in self.listaKlientow[wyobr-1].samochodyKliena:
            x.ustawWlasciciela('brak')
            self.listaSamochodow.append(x)
            self.samochodyWypozyczone.remove(x)
        self.listaKlientow.remove(self.listaKlientow[wyobr-1])

    #Funkcja dodająca samochód do bazy
    def dodajSamochod(self):
        marka = input('Marka: ')
        model = input('Model: ')
        rocznik = input('Rocznik: ')
        try:

            self.listaSamochodow.append(Samochod(marka,model,rocznik))
            print('Dodano samochód!')
        except ValueError:
            print('Błąd przy dodawaniu samochodu!')

    #Funkcja usuwająca samochód z bazy
    def usunSamochod(self):
        print('Wybierz który samochód chcesz usunąć: ')
        self.wyswietlListeSamochodow()
        wyobr = int(input('Wybór: '))
        self.listaSamochodow.remove(self.listaSamochodow[wyobr - 1])

#Stworzenie klasy Samochód
class Samochod:
    marka = ''
    model = ''
    rocznik = 0
    wypozyczonyPrzez = 'brak'
    koszt = 0

    #Konstruktor
    def __init__(self, marka, model, rocznik, koszt):
        self.marka = marka
        self.model = model
        self.rocznik = rocznik
        self.koszt = koszt

    #Funkcja odpowiedzialna za wypisanie informacji o samochodzie
    def informacjeSamochod(self):
        return self.model + ' ' + self.marka + ' ' + str(self.rocznik) + 'r. - wypożyczony przez: ' + self.wypozyczonyPrzez + ' cena: ' + str(self.koszt) + ' PLN'

    #Funkcja umożliwiająca zmianę właściciela
    def ustawWlasciciela(self, wlasciciel):
        self.wypozyczonyPrzez = str(wlasciciel)

#Stworzenie klasy Klient
class Klient:
    imie = ''
    nazwisko = ''
    wiek = 0
    saldo = 0

    #Konstruktor
    def __init__(self, imie, nazwisko, wiek, saldo):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.samochodyKliena = []
        self.saldo = saldo

    def dodajSrodki(self, ilosc):
        self.saldo += ilosc

    def odejmijSrodki(self, ilosc):
        self.saldo -= ilosc

    #Funkcja odpowiedzialna za wypisanie informacji o użytkowniku
    def informacjeKlient(self):
        info = self.imie
        info += ' '+ self.nazwisko
        info += ' wiek: '+ str(self.wiek)
        info += ' SALDO: ' + str(self.saldo)
        info += '\n   Lista samochodów (' + str(len(self.samochodyKliena)) + ' szt.):'
        for x in self.samochodyKliena:
            info += '\n     '
            info += x.informacjeSamochod()
        return info

    #Funkcja odpowiedzialna za wynajem auta (samochód zostaje dodany do listy aut użytkownika oraz do listy wypożyczonych aut (ogólnych)
    def wypozyczSamochod(self):
        index = 1
        print('Wybierz samochód z listy:')
        for x in baza.listaSamochodow:
            print(index, x.informacjeSamochod())
            index += 1
        nr = int(input('Wybór: '))
        if baza.listaSamochodow[nr - 1].koszt <= self.saldo:
            try:
                self.samochodyKliena.append(baza.listaSamochodow[nr-1])
                self.odejmijSrodki(baza.listaSamochodow[nr - 1].koszt)
                baza.samochodyWypozyczone.append(baza.listaSamochodow[nr - 1])
                baza.listaSamochodow[nr - 1].ustawWlasciciela(self.nazwisko)
                baza.listaSamochodow.remove(baza.listaSamochodow[nr-1])
                print('Pomyśnie wypożyczono samochód!')
            except ValueError:
                print('Nie udało się dodać samochodu do klienta!')
        else:
            print('Klient nie ma wystarczających środków!')

    #Usuwanie wypożyczenia (przywrócenie samochodu do początkowej listy)
    def usunWypozyczenie(self):
        index = 1
        print('Wybierz samochód z listy:')
        for x in self.samochodyKliena:
            print(index, str(x.informacjeSamochod()))
            index += 1
        nr = int(input('Wybór: '))
        print(nr)
        try:
            baza.listaSamochodow.append(self.samochodyKliena[nr-1])
            baza.samochodyWypozyczone.remove(self.samochodyKliena[nr-1])
            self.samochodyKliena[nr - 1].ustawWlasciciela('brak')
            self.samochodyKliena.remove(self.samochodyKliena[nr-1])
        except ValueError:
            print('Nie udało się usunąć!')

#Stowrzenie bazy
baza = Baza()

#Funkcja która uzupełnia baze przykładowymi danymi
def stworzPrzykladowaBaze():
    klient1 = Klient('Jarosław', 'Klek', 50, 2000)
    klient2 = Klient('Sebastian', 'Esame', 12, 3000)
    klient3 = Klient('Michał', 'Rafon', 23, 100)
    klient4 = Klient('Zacho', 'Ość', 11, 21)

    samochod1 = Samochod('Audi', 'A3', 1998, 1000)
    samochod2 = Samochod('BMW', 'E36', 1999, 200)
    samochod3 = Samochod('Opel', 'Meriva', 2004, 1100)
    samochod4 = Samochod('Renault', 'Clio', 2015, 500)

    baza.listaKlientow.append(klient1)
    baza.listaKlientow.append(klient2)
    baza.listaKlientow.append(klient3)
    baza.listaKlientow.append(klient4)

    baza.listaSamochodow.append(samochod1)
    baza.listaSamochodow.append(samochod2)
    baza.listaSamochodow.append(samochod3)
    baza.listaSamochodow.append(samochod4)

#Wyświetlanie MENU
def menu():
    while True:
        print('Witaj w wypożyczalni ESAME!\nWybierz co chcesz zrobić:\n'
              '1. Zarządzaj klientami\n'
              '2. Zarządzaj samochodami\n'
              '3. Wyjście')
        wybor = int(input('Wybór: '))
        try:
            if wybor == 1:
                menuKlienta()
            elif wybor == 2:
                menuSamochody()
            elif wybor == 3:
                exit(0)
        except ValueError:
            print('Błąd przy wyborze!')

#Menu klienta
def menuKlienta():
    while True:
        print('----------\n'
              '1. Lista użytkowników\n'
              '2. Dodaj użytkownika\n'
              '3. Usuń użytkownika\n'
              '4. Dodaj wypożyczenie\n'
              '5. Usuń wypożyczenie\n'
              '6. Dodaj środki\n'
              '7. Nałóż karę pieniężną\n'
              '8. Menu')
        wybor = int(input('Wybór: '))
        if wybor == 1:
            baza.wyswietlListeKlientow()
        elif wybor == 2:
            baza.dodajKlienta()
        elif wybor == 3:
            baza.usunKlienta()
        elif wybor == 4:
            print('Wybierz klienta:')
            baza.wyswietlListeKlientow()
            tmp = int(input('Podaj pozycję klienta: '))
            baza.listaKlientow[tmp - 1].wypozyczSamochod()
        elif wybor == 5:
            print('Wybierz klienta:')
            baza.wyswietlListeKlientow()
            tmp = int(input('Podaj pozycję klienta: '))
            baza.listaKlientow[tmp - 1].usunWypozyczenie()
        elif wybor == 6:
            print('Wybierz klienta:')
            baza.wyswietlListeKlientow()
            tmp = int(input('Podaj pozycję klienta: '))
            kwota = int(input('Jaką kwotą chcesz doładować konto: '))
            baza.listaKlientow[tmp - 1].dodajSrodki(kwota)
        elif wybor == 7:
            print('Wybierz klienta:')
            baza.wyswietlListeKlientow()
            tmp = int(input('Podaj pozycję klienta: '))
            kwota = int(input('Jaką karę chcesz nałożyć na konto: '))
            baza.listaKlientow[tmp - 1].odejmijSrodki(kwota)
        elif wybor == 8:
            menu()

#Menu samochody
def menuSamochody():
    while True:
        print('----------\n'
              '1. Lista samochodów dostępnych\n'
              '2. Lista wypożyczonych samochodów\n'
              '3. Dodaj samochód\n'
              '4. Usuń samochód\n'
              '5. Menu')
        wybor = int(input('Wybór: '))
        if wybor == 1:
            baza.wyswietlListeSamochodow()
        elif wybor == 2:
            baza.wyswietlListeSamochodowWypozyczonych()
        elif wybor == 3:
            baza.dodajSamochod()
        elif wybor == 4:
            baza.usunSamochod()
        elif wybor == 5:
            menu()

stworzPrzykladowaBaze()
menu()