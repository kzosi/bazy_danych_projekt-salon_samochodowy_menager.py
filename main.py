from tkinter import *
import mysql.connector
from tkinter import ttk
from PIL import ImageTk, Image


root = Tk()
root.title("Salon samochodowy menager")
root.iconbitmap('d:/gui/car.ico')
root.geometry("1000x900")



db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="231qqqXD1",
    database="salonsamochodowy"

)

cursor = db.cursor()


fr = Frame(root)
fr.pack(side="top", expand=True, fill="both")


def wlasciciele():

    def clearwl():
        b1.delete(0, END)
        b2.delete(0, END)
        b3.delete(0, END)


    def addwl():
        sqlcomand = "INSERT INTO wlasciciel (imie, nazwisko, pesel) VALUES (%s,%s,%s)"
        val = (b1.get(), b2.get(), b3.get())
        cursor.execute(sqlcomand, val)

        db.commit()
        wlasciciele()

    def searchwl():

        def griddy():
            entrybox = Entry(ser)
            entrybox.grid(row=0, column=1, padx=10, pady=10)

            searchlbl = Label(ser, text="Szukaj właścicieli")
            searchlbl.grid(row=0, column=0, padx=10, pady=10)

            dropbox = ttk.Combobox(ser, values=['Szukaj po.. ', 'Imie', 'Nazwisko', 'Pesel'])
            dropbox.current(0)
            dropbox.grid(row=0, column=2)

            shbutton = Button(ser, text="szukaj", command=lambda: searchnow(entrybox.get(), dropbox.get()))
            shbutton.grid(row=1, column=0)

        def editrec(id):

            def update(id, new_imie, new_nazwisko, new_pesel):
                sqlcomand = "UPDATE wlasciciel SET imie = %s, nazwisko = %s, pesel = %s WHERE wlascicielID = %s;"
                val = (new_imie, new_nazwisko, new_pesel, id)
                cursor.execute(sqlcomand, val)
                db.commit()

                ed.destroy()
                wlasciciele()

            ed = Tk()
            ed.title("Edytowanie")
            ed.iconbitmap('d:/gui/car.ico')
            ed.geometry("1000x800")

            ll = Label(ed, text="Edycja rekordu w tabeli: Właściciele", font=("Arial", 12, 'bold'))
            ll.grid(row=0, column=1, columnspan=3, sticky=W)

            l1 = Label(ed, text="Imie", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            l2 = Label(ed, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            l3 = Label(ed, text="Pesel", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)

            b1 = Entry(ed)
            b1.grid(column=2, row=2)
            b2 = Entry(ed)
            b2.grid(column=2, row=3)
            b3 = Entry(ed)
            b3.grid(column=2, row=4)


            addmodel = Button(ed, text="Zatwierdź", padx=20, pady=10,command=lambda: update(id, b1.get(), b2.get(), b3.get()))
            addmodel.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            clrr = Button(ed, text="Wyczyść", padx=20, pady=10, command=clearmodel)
            clrr.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def deleterec(id):
            sql = "DELETE FROM wlasciciel WHERE wlascicielID = %s"
            name = (id,)
            result = cursor.execute(sql, name)
            result = cursor.fetchall()
            db.commit()

            for widgets in ser.winfo_children():
                widgets.destroy()
            griddy()
            sprzedawcy()

        def searchnow(par, selected):

            for widgets in ser.winfo_children():
                widgets.destroy()

            griddy()

            sql = ''
            if selected == 'Imie':
                sql = "SELECT * FROM wlasciciel WHERE imie = %s"
            if selected == 'Nazwisko':
                sql = "SELECT * FROM wlasciciel WHERE nazwisko = %s"
            if selected == 'Pesel':
                sql = "SELECT * FROM wlasciciel WHERE pesel = %s"

            name = (par,)
            result = cursor.execute(sql, name)
            result = cursor.fetchall()

            if not result:
                result = "nie znaleziono"
                l000 = Label(ser, text=result, font=('arial', 10, "bold")).grid(column=0, row=2)

            else:
                l000 = Label(ser, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2)
                l111 = Label(ser, text="Imię", font=('arial', 10, "bold")).grid(column=3, row=2)
                l222 = Label(ser, text="Nazwisko", font=('arial', 10, "bold")).grid(column=4, row=2)
                l333 = Label(ser, text="Pesel", font=('arial', 10, "bold")).grid(column=5, row=2)

                for index, x in enumerate(result):
                    position = 0
                    index += 3
                    id_ref = x[0]
                    edit_button = Button(ser, text="Edytuj", command=lambda: editrec(id_ref))
                    delete_button = Button(ser, text='Usuń', command=lambda: deleterec(id_ref))
                    edit_button.grid(row=index, column=position)
                    delete_button.grid(row=index, column=position + 1)

                    for y in x:
                        dblabel = Label(ser, text=y)
                        dblabel.grid(row=index, column=position + 2)
                        position += 1

        ser = Tk()
        ser.title("Szukaj w właściciele")
        ser.iconbitmap('d:/gui/car.ico')
        ser.geometry("1000x800")
        griddy()

    clear_frame()
    root.title("Salon samochodowy menager - Właściciele")
    bck = Button(fr, text="<<", padx=10, pady=5, command=start_screen)
    bck.grid(row=0, column=0,sticky=W)
    ll = Label(fr, text="Dodaj do bazy danych (Właściciele):", font=("Arial", 12,'bold'))
    ll.grid(row=0, column=1,columnspan=3,sticky=W)

    l1 = Label(fr, text="Imię",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    l2 = Label(fr, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    l3 = Label(fr, text="Pesel", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)

    b1 = Entry(fr)
    b1.grid(column=2, row=2)
    b2 = Entry(fr)
    b2.grid(column=2, row=3)
    b3 = Entry(fr)
    b3.grid(column=2, row=4)


    addwlasciciel = Button(fr, text="Dodaj", padx=20, pady=10, command=addwl)
    addwlasciciel.grid(column=1, row=6, sticky=W, padx=20, pady=20)
    clrr = Button(fr, text="Wyczyść", padx=20, pady=10, command=clearwl)
    clrr.grid(column=2, row=6, sticky=W, padx=20, pady=20)
    search = Button(fr, text="Szukaj w bazie danych", padx=20, pady=10, command=searchwl)
    search.grid(column=3, row=6, sticky=W, padx=20, pady=20)


    podgladinfo = Label(fr, text="Podgląd bazy danych", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=3)

    l00 = Label(fr, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8)
    l11 = Label(fr, text="Imie", font=('arial', 10, "bold")).grid(column=1, row=8)
    l22 = Label(fr, text="Nazwisko", font=('arial', 10, "bold")).grid(column=2, row=8)
    l33 = Label(fr, text="Pesel", font=('arial', 10, "bold")).grid(column=3, row=8)

    cursor.execute("SELECT * FROM wlasciciel")
    result = cursor.fetchall()

    for index, x in enumerate(result):
        position = 0
        for y in x:
            dblabel = Label(fr, text=y)
            dblabel.grid(row=index + 9, column=position)
            position += 1

def sprzedawcy():
    def clearsp():
        b1.delete(0, END)
        b2.delete(0, END)
        b3.delete(0, END)


    def addsp():
        sqlcomand = "INSERT INTO sprzedawca (imie, nazwisko, stanowisko) VALUES (%s,%s,%s)"
        val = (b1.get(), b2.get(), b3.get())
        cursor.execute(sqlcomand, val)

        db.commit()
        sprzedawcy()

    def searchsp():

        def griddy():
            entrybox = Entry(ser)
            entrybox.grid(row=0, column=1, padx=10, pady=10)

            searchlbl = Label(ser, text="Szukaj sprzedawców")
            searchlbl.grid(row=0, column=0, padx=10, pady=10)

            dropbox = ttk.Combobox(ser, values=['Szukaj po.. ', 'Imie', 'Nazwisko', 'Stanowisko'])
            dropbox.current(0)
            dropbox.grid(row=0, column=2)

            shbutton = Button(ser, text="szukaj", command=lambda: searchnow(entrybox.get(), dropbox.get()))
            shbutton.grid(row=1, column=0)

        def editrec(id):

            def update(id, new_imie, new_nazwisko, new_stanowisko):
                sqlcomand = "UPDATE sprzedawca SET imie = %s, nazwisko = %s, stanowisko = %s WHERE wlascicielID = %s;"
                val = (new_imie, new_nazwisko, new_stanowisko, id)
                cursor.execute(sqlcomand, val)
                db.commit()

                ed.destroy()
                sprzedawcy()

            ed = Tk()
            ed.title("Edytowanie")
            ed.iconbitmap('d:/gui/car.ico')
            ed.geometry("1000x800")

            ll = Label(ed, text="Edycja rekordu w tabeli: Sprzedawcy", font=("Arial", 12, 'bold'))
            ll.grid(row=0, column=1, columnspan=3, sticky=W)

            l1 = Label(ed, text="Imie", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            l2 = Label(ed, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            l3 = Label(ed, text="Stanowisko", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)

            b1 = Entry(ed)
            b1.grid(column=2, row=2)
            b2 = Entry(ed)
            b2.grid(column=2, row=3)
            b3 = Entry(ed)
            b3.grid(column=2, row=4)


            addmodel = Button(ed, text="Zatwierdź", padx=20, pady=10,command=lambda: update(id, b1.get(), b2.get(), b3.get()))
            addmodel.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            clrr = Button(ed, text="Wyczyść", padx=20, pady=10, command=clearmodel)
            clrr.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def deleterec(id):
            sql = "DELETE FROM sprzedawca WHERE sprzedawcaID = %s"
            name = (id,)
            result = cursor.execute(sql, name)
            result = cursor.fetchall()
            db.commit()

            for widgets in ser.winfo_children():
                widgets.destroy()
            griddy()
            sprzedawcy()

        def searchnow(par, selected):

            for widgets in ser.winfo_children():
                widgets.destroy()

            griddy()

            sql = ''
            if selected == 'Imie':
                sql = "SELECT * FROM sprzedawca WHERE imie = %s"
            if selected == 'Nazwisko':
                sql = "SELECT * FROM sprzedawca WHERE nazwisko = %s"
            if selected == 'Stanowisko':
                sql = "SELECT * FROM sprzedawca WHERE stanowisko = %s"

            name = (par,)
            result = cursor.execute(sql, name)
            result = cursor.fetchall()

            if not result:
                result = "nie znaleziono"
                l000 = Label(ser, text=result, font=('arial', 10, "bold")).grid(column=0, row=2)

            else:
                l000 = Label(ser, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2)
                l111 = Label(ser, text="Imię", font=('arial', 10, "bold")).grid(column=3, row=2)
                l222 = Label(ser, text="Nazwisko", font=('arial', 10, "bold")).grid(column=4, row=2)
                l333 = Label(ser, text="Stanowisko", font=('arial', 10, "bold")).grid(column=5, row=2)

                for index, x in enumerate(result):
                    position = 0
                    index += 3
                    id_ref = x[0]
                    edit_button = Button(ser, text="Edytuj", command=lambda: editrec(id_ref))
                    delete_button = Button(ser, text='Usuń', command=lambda: deleterec(id_ref))
                    edit_button.grid(row=index, column=position)
                    delete_button.grid(row=index, column=position + 1)

                    for y in x:
                        dblabel = Label(ser, text=y)
                        dblabel.grid(row=index, column=position + 2)
                        position += 1

        ser = Tk()
        ser.title("Szukaj w sprzedawcy")
        ser.iconbitmap('d:/gui/car.ico')
        ser.geometry("1000x800")
        griddy()

    clear_frame()
    root.title("Salon samochodowy menager - Sprzedawcy")
    bck = Button(fr, text="<<", padx=10, pady=5, command=start_screen)
    bck.grid(row=0, column=0,sticky=W)
    ll = Label(fr, text="Dodaj do bazy danych (Sprzedawcy):", font=("Arial", 12,'bold'))
    ll.grid(row=0,column=1,columnspan=3,sticky=W)

    l1 = Label(fr, text="Imię",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    l2 = Label(fr, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    l3 = Label(fr, text="Stanowisko", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)

    b1 = Entry(fr)
    b1.grid(column=2, row=2)
    b2 = Entry(fr)
    b2.grid(column=2, row=3)
    b3 = Entry(fr)
    b3.grid(column=2, row=4)


    addsprzedawca = Button(fr, text="Dodaj", padx=20, pady=10, command=addsp)
    addsprzedawca.grid(column=1, row=6, sticky=W, padx=20, pady=20)
    clrr = Button(fr, text="Wyczyść", padx=20, pady=10, command=clearsp)
    clrr.grid(column=2, row=6, sticky=W, padx=20, pady=20)
    search = Button(fr, text="Szukaj w bazie danych", padx=20, pady=10, command=searchsp)
    search.grid(column=3, row=6, sticky=W, padx=20, pady=20)

    podgladinfo = Label(fr, text="Podgląd bazy danych", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=3)

    l00 = Label(fr, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8)
    l11 = Label(fr, text="Imie", font=('arial', 10, "bold")).grid(column=1, row=8)
    l22 = Label(fr, text="Nazwisko", font=('arial', 10, "bold")).grid(column=2, row=8)
    l33 = Label(fr, text="Stanowisko", font=('arial', 10, "bold")).grid(column=3, row=8)

    cursor.execute("SELECT * FROM sprzedawca")
    result = cursor.fetchall()

    for index, x in enumerate(result):
        position = 0
        for y in x:
            dblabel = Label(fr, text=y)
            dblabel.grid(row=index + 9, column=position)
            position += 1

def samochody():
    def clearsam():
        b1.delete(0, END)
        b2.delete(0, END)
        b3.delete(0, END)
        b4.delete(0, END)

    def addsam():
        sqlcomand = "INSERT INTO samochod (VIN, modelID, sprzedawcaID, wlascicielID) VALUES (%s,%s,%s,%s)"
        val = (b1.get(), b2.get(), b3.get(), b4.get())
        cursor.execute(sqlcomand, val)

        db.commit()
        samochody()

    clear_frame()
    root.title("Salon samochodowy menager - Samochody")
    bck = Button(fr, text="<<", padx=20, pady=5, command=start_screen)
    bck.grid(row=0, column=0,sticky=W)
    ll = Label(fr, text="Dodaj do bazy danych (Samochody):", font=("Arial", 12,'bold'),)
    ll.grid(row=0, column=1,columnspan=3)

    l1 = Label(fr, text="VIN",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    l2 = Label(fr, text="ID modelu", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    l3 = Label(fr, text="ID sprzedawcy", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)
    l4 = Label(fr, text="ID właściciela", font=("Arial", 12)).grid(column=1, row=5, sticky=W, padx=5, pady=10)

    b1 = Entry(fr)
    b1.grid(column=2, row=2,sticky=W)
    b2 = Entry(fr)
    b2.grid(column=2, row=3,sticky=W)
    b3 = Entry(fr)
    b3.grid(column=2, row=4,sticky=W)
    b4 = Entry(fr)
    b4.grid(column=2, row=5,sticky=W)

    addsamochod = Button(fr, text="Dodaj", padx=5, pady=10, command=addsam)
    addsamochod.grid(column=1, row=6, sticky=W, padx=5, pady=20)
    clrr = Button(fr, text="Wyczyść", padx=5, pady=10, command=clearsam)
    clrr.grid(column=2, row=6, sticky=W, padx=5, pady=20)

    podgladinfo = Label(fr, text="Podgląd bazy danych", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=3)

    l00 = Label(fr, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8,sticky=W)
    l11 = Label(fr, text="VIN", font=('arial', 10, "bold")).grid(column=1, row=8,sticky=W)
    l22 = Label(fr, text="Marka", font=('arial', 10, "bold")).grid(column=2, row=8,sticky=W)
    l33 = Label(fr, text="Model", font=('arial', 10, "bold")).grid(column=3, row=8,sticky=W)
    l44 = Label(fr, text="Właściciel", font=('arial', 10, "bold")).grid(column=4, row=8,sticky=W)
    l44 = Label(fr, text="Sprzedawca", font=('arial', 10, "bold")).grid(column=6, row=8, sticky=W)

    cursor.execute("SELECT samochod.samochodID, samochod.VIN, model.marka ,model.nazwa, wlasciciel.imie, wlasciciel.nazwisko, sprzedawca.imie, sprzedawca.nazwisko FROM (((samochod INNER JOIN model ON samochod.modelID = model.modelID) INNER JOIN sprzedawca ON samochod.sprzedawcaID = sprzedawca.sprzedawcaID) INNER JOIN wlasciciel ON samochod.wlascicielID = wlasciciel.wlascicielID);")
    result = cursor.fetchall()

    for index, x in enumerate(result):
        position = 0
        for y in x:
            dblabel = Label(fr, text=y)
            dblabel.grid(row=index + 9, column=position,sticky=W)
            position += 1

def modele():

    def clearmodel():
        b1.delete(0, END)
        b2.delete(0, END)
        b3.delete(0, END)
        b4.delete(0, END)

    def addmode():
        sqlcomand = "INSERT INTO model (marka, nazwa, rok_produkcji, nadwozie) VALUES (%s,%s,%s,%s)"
        val = (b1.get(), b2.get(), b3.get(), b4.get())
        cursor.execute(sqlcomand, val)

        db.commit()
        modele()

    def searchmod():

        def griddy():
            entrybox = Entry(ser)
            entrybox.grid(row=0, column=1, padx=10, pady=10)

            searchlbl = Label(ser, text="Szukaj sprzedawcow")
            searchlbl.grid(row=0, column=0, padx=10, pady=10)


            dropbox = ttk.Combobox(ser, values=['Szukaj po.. ', 'Marka', 'Nazwa','Rok Produkcji', 'Nadwozie'])
            dropbox.current(0)
            dropbox.grid(row=0, column=2)

            shbutton = Button(ser, text="szukaj",command=lambda:searchnow(entrybox.get(), dropbox.get()))
            shbutton.grid(row=1, column =0)

        def editrec(id):

            def update(id, new_marka, new_nazwa, new_rok_produkcji, new_nadwozie):

                sqlcomand = "UPDATE model SET marka = %s, nazwa = %s, rok_produkcji = %s,nadwozie = %s WHERE modelID = %s;"
                val = (new_marka, new_nazwa, new_rok_produkcji, new_nadwozie,id)
                cursor.execute(sqlcomand, val)
                db.commit()

                ed.destroy()
                modele()



            ed = Tk()
            ed.title("Edytowanie")
            ed.iconbitmap('d:/gui/car.ico')
            ed.geometry("1000x800")

            ll = Label(ed, text="Edycja rekordu w tabeli: Modele", font=("Arial", 12, 'bold'))
            ll.grid(row=0, column=1, columnspan=3, sticky=W)

            l1 = Label(ed, text="Marka", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            l2 = Label(ed, text="Nazwa", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            l3 = Label(ed, text="Rok produkcji", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)
            l4 = Label(ed, text="Nadwozie", font=("Arial", 12)).grid(column=1, row=5, sticky=W, padx=5, pady=10)

            b1 = Entry(ed)
            b1.grid(column=2, row=2)
            b2 = Entry(ed)
            b2.grid(column=2, row=3)
            b3 = Entry(ed)
            b3.grid(column=2, row=4)
            b4 = Entry(ed)
            b4.grid(column=2, row=5)

            addmodel = Button(ed, text="Zatwierdź", padx=20, pady=10, command=lambda:update(id,b1.get(),b2.get(),b3.get(),b4.get()))
            addmodel.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            clrr = Button(ed, text="Wyczyść", padx=20, pady=10, command=clearmodel)
            clrr.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def deleterec(id):
            sql = "DELETE FROM model WHERE modelID = %s"
            name = (id,)
            result = cursor.execute(sql, name)
            result = cursor.fetchall()
            db.commit()

            for widgets in ser.winfo_children():
                widgets.destroy()
            griddy()
            modele()


        def searchnow(par,selected):

            for widgets in ser.winfo_children():
                widgets.destroy()

            griddy()

            sql = ''
            if selected == 'Nadwozie':
                sql = "SELECT * FROM model WHERE nadwozie = %s"
            if selected == 'Nazwa':
                sql = "SELECT * FROM model WHERE nazwa = %s"
            if selected == 'Marka':
                sql = "SELECT * FROM model WHERE marka = %s"
            if selected == 'Rok Produkcji':
                sql = "SELECT * FROM model WHERE rok_produkcji = %s"

            name = (par,)
            result = cursor.execute(sql, name)
            result = cursor.fetchall()

            if not result:
                result = "nie znaleziono"
                l000 = Label(ser, text=result, font=('arial', 10, "bold")).grid(column=0, row=2)

            else:
                l000 = Label(ser, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2)
                l111 = Label(ser, text="Marka", font=('arial', 10, "bold")).grid(column=3, row=2)
                l222 = Label(ser, text="Nazwa", font=('arial', 10, "bold")).grid(column=4, row=2)
                l333 = Label(ser, text="Rok produkcji", font=('arial', 10, "bold")).grid(column=5, row=2)
                l444 = Label(ser, text="Nadwozie", font=('arial', 10, "bold")).grid(column=6, row=2)

                for index, x in enumerate(result):
                    position = 0
                    index += 3
                    id_ref = x[0]
                    edit_button = Button(ser, text="Edytuj", command=lambda:editrec(id_ref))
                    delete_button =Button(ser,text='Usuń', command=lambda: deleterec(id_ref))
                    edit_button.grid(row=index, column=position)
                    delete_button.grid(row=index, column=position+1)

                    for y in x:
                        dblabel = Label(ser, text=y)
                        dblabel.grid(row=index, column=position+2)
                        position += 1




        ser = Tk()
        ser.title("Szukaj w modele")
        ser.iconbitmap('d:/gui/car.ico')
        ser.geometry("1000x800")
        griddy()




    clear_frame()
    root.title("Salon samochodowy menager - Modele")
    bck = Button(fr, text="<<", padx=10, pady=5, command=start_screen)
    bck.grid(row=0, column=0,sticky=W)
    ll = Label(fr, text="Dodaj do bazy danych (Modele):", font=("Arial", 12, 'bold'))
    ll.grid(row=0, column=1,columnspan=3,sticky=W)

    l1 = Label(fr, text="Marka",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    l2 = Label(fr, text="Nazwa", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    l3 = Label(fr, text="Rok produkcji", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)
    l4 = Label(fr, text="Nadwozie", font=("Arial", 12)).grid(column=1, row=5, sticky=W, padx=5, pady=10)

    b1 = Entry(fr)
    b1.grid(column=2, row=2)
    b2 = Entry(fr)
    b2.grid(column=2, row=3)
    b3 = Entry(fr)
    b3.grid(column=2, row=4)
    b4 = Entry(fr)
    b4.grid(column=2, row=5)

    addmodel = Button(fr, text="Dodaj", padx=20, pady=10, command=addmode)
    addmodel.grid(column=1, row=6, sticky=W, padx=20, pady=20)
    clrr = Button(fr, text="Wyczyść", padx=20, pady=10, command=clearmodel)
    clrr.grid(column=2, row=6, sticky=W, padx=20, pady=20)
    search = Button(fr, text="Szukaj w bazie danych", padx=20, pady=10, command=searchmod)
    search.grid(column=3, row=6, sticky=W, padx=20, pady=20)

    podgladinfo = Label(fr, text="Podgląd bazy danych", font=("Arial", 12,'bold')).grid(column=0, row=7, sticky=W, padx=5, pady=10,columnspan=3)

    l00 = Label(fr, text="ID",font=('arial',10,"bold")).grid(column=0, row=8)
    l11 = Label(fr, text="Marka",font=('arial',10,"bold")).grid(column=1, row=8)
    l22 = Label(fr, text="Nazwa",font=('arial',10,"bold")).grid(column=2, row=8)
    l33 = Label(fr, text="Rok produkcji",font=('arial',10,"bold")).grid(column=3, row=8)
    l44 = Label(fr, text="Nadwozie",font=('arial',10,"bold")).grid(column=4, row=8)

    cursor.execute("SELECT * FROM model")
    result = cursor.fetchall()

    for index,x in enumerate(result):
        position = 0
        for y in x:
            dblabel = Label(fr, text=y)
            dblabel.grid(row=index+9,column=position)
            position+=1


def clear_frame():
    for widgets in fr.winfo_children():
        widgets.destroy()


def start_screen():
    clear_frame()
    root.title("Salon samochodowy menager")
    start = Label(fr, text="Witaj w salon samochodowy - database menager", font=("Arial", 30)).pack()
    img = ImageTk.PhotoImage(Image.open('d:/gui/zygzak.jpg'))
    img_lbl = Label(fr,image=img)
    img_lbl.image = img
    img_lbl.pack()

    st = Label(fr, text="Wybierz tabelę", font=("Arial", 20)).pack()
    b1 = Button(fr, text="Samochody", padx=26, pady=20, command=samochody).pack()
    b2 = Button(fr, text="Właściciele", padx=29, pady=20, command=wlasciciele).pack()
    b3 = Button(fr, text="Sprzedawcy", padx=29, pady=20, command=sprzedawcy).pack()
    b4 = Button(fr, text="Modele", padx=40, pady=20, command=modele).pack()


start_screen()

root.mainloop()