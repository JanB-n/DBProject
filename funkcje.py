from psycopg2 import connect, sql

def stworz_magazyn(conn, nazwa, kraj, miasto, ulica, numer, kod):
    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Magazyn\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w 'znajdz_id: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Magazyn\" VALUES (\'{current_id}\', \'{nazwa}\', \'{kraj}\', \'{miasto}\', \'{ulica}\', \'{numer}\', \'{kod}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_magazyn: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_magazyny(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT * FROM \"Magazyn\"")

    try:
        cursor.execute(sql_object)
        mags = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_magazyny:", e)
        conn.rollback()
        mags = []
    finally:
        cursor.close()

    return mags

def get_dzialyall(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT DISTINCT nazwa FROM \"Dzial\"")

    try:
        cursor.execute(sql_object)
        mags = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_dzialyall:", e)
        conn.rollback()
        mags = []
    finally:
        cursor.close()

    return mags

def get_osoby(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT DISTINCT id, imie, nazwisko FROM \"Pracownik\"")

    try:
        cursor.execute(sql_object)
        mags = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_osoby:", e)
        conn.rollback()
        mags = []
    finally:
        cursor.close()

    return mags

def stworz_pracownik(conn, imie, nazwisko, rola, mag):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Magazyn\" WHERE nazwa = \'{mag}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: znajdz_id magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Pracownik\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w stworz_dzial: znajdz_id dla dzialu: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Pracownik\" VALUES (\'{current_id}\', \'{mag_id}\', \'{rola}\', \'{imie}\', \'{nazwisko}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_dzial: dodawanie do bazy: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def stworz_dzial(conn, nazwa, mag):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Magazyn\" WHERE nazwa = \'{mag}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: znajdz_id magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Dzial\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w stworz_dzial: znajdz_id dla dzialu: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Dzial\" VALUES (\'{current_id}\', \'{mag_id}\', \'{nazwa}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_dzial: dodawanie do bazy: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_dzialy(conn, mag):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Magazyn\" WHERE nazwa = \'{mag}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w get_dzialy: znajdz_id magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
    
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Dzial\" WHERE id_magazyn = {mag_id}")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        dzialy = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_dzialy: znajdz_id dzialu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    return dzialy

def stworz_polke(conn, Mag, Dzial, Regal, Polka):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Magazyn\" WHERE nazwa = \'{Mag}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    nowydzial = False

    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Dzial\" WHERE nazwa = \'{Dzial}\' AND id_magazyn = {mag_id} LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        dzial_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke dla dzialu: ", e)
        conn.rollback()
        try:
            stworz_dzial(conn, Dzial, Mag)
            print("Stworzono nowy dzial:", Mag, Dzial)
            nowydzial = True
        except Exception as e:
            print("Blad w tworzeniu nowego dzialu:", e)
    finally:
        cursor.close()

    if nowydzial:
        cursor = conn.cursor()
        find_id = sql.SQL(f"SELECT * FROM \"Dzial\" WHERE nazwa = \'{Dzial}\' AND id_magazyn = {mag_id} LIMIT 1")
        try:
            cursor.execute(find_id)
            conn.commit()
            dzial_id = int(cursor.fetchone()[0])
        except Exception as e:
            print ("ERROR w stworz_dzial: stworz_polke dla dzialu: ", e)
            conn.rollback()
            return False
        finally:
            cursor.close()


    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Polozenie\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke dla Polozenie: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Polozenie\" VALUES (\'{current_id}\', {Regal}, {Polka}, \'{dzial_id}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke dodawanie do bazy: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def stworz_klienta(conn, nazwa, NIP, REGON, adres, typ, telefon):
    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Klient\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w 'znajdz_id: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Klient\" VALUES (\'{current_id}\', \'{nazwa}\', \'{NIP}\', \'{REGON}\', \'{adres}\', \'{typ}\', {telefon})")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_magazyn: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
    
def get_klienci(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT * FROM \"Klient\"")

    try:
        cursor.execute(sql_object)
        mags = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_klienci:", e)
        conn.rollback()
        mags = []
    finally:
        cursor.close()

    return mags

def get_wszystkiedzialy(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT * FROM \"Dzial\"")

    try:
        cursor.execute(sql_object)
        dzialy = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_klienci:", e)
        conn.rollback()
        dzialy = []
    finally:
        cursor.close()

    magazyny =  {}
    
    for dzial in dzialy:
        cursor = conn.cursor()

        sql_object = sql.SQL(f"SELECT nazwa FROM \"Magazyn\" WHERE id = {dzial[1]} LIMIT 1")

        try:
            cursor.execute(sql_object)
            nazwa_magazynu = cursor.fetchone()[0]
        except Exception as e:
            print ("ERROR w nazwie magazynu:", e)
            conn.rollback()
            nazwa_magazynu = ""
        finally:
            cursor.close()
        magazyny[dzial[1]] = nazwa_magazynu

    return dzialy, magazyny

def get_wszyscypracownicy(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT * FROM \"Pracownik\"")

    try:
        cursor.execute(sql_object)
        pracownicy = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_klienci:", e)
        conn.rollback()
        pracownicy = []
    finally:
        cursor.close()

    magazyny =  {}
    
    for pracownik in pracownicy:
        cursor = conn.cursor()

        sql_object = sql.SQL(f"SELECT nazwa FROM \"Magazyn\" WHERE id = {pracownik[1]} LIMIT 1")

        try:
            cursor.execute(sql_object)
            nazwa_magazynu = cursor.fetchone()[0]
        except Exception as e:
            print ("ERROR w nazwie magazynu:", e)
            conn.rollback()
            nazwa_magazynu = ""
        finally:
            cursor.close()
        magazyny[pracownik[1]] = nazwa_magazynu

    return pracownicy, magazyny

def dodaj_wozek(conn, id_dzial, producent, nosnosc):
    cursor = conn.cursor()
    find_dzial = sql.SQL(f"SELECT * FROM \"Wozek\" WHERE id_dzial = {id_dzial} LIMIT 1")
    try:
        cursor.execute(find_dzial)
        conn.commit()
        found = cursor.fetchall()
    except Exception as e:
        print ("ERROR w wozek znajdz_id: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
    
    if(found == None):
        return False
    
    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Wozek\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w wozek znajdz_id: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Wozek\" VALUES (\'{current_id}\', {id_dzial}, {nosnosc}, \'{producent}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w dodaj_wozek: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_wozki(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT * FROM \"Wozek\"")

    try:
        cursor.execute(sql_object)
        wozki = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_wozki:", e)
        conn.rollback()
        wozki = []
    finally:
        cursor.close()
    
    new_wozki = []
    
    for wozek in wozki:
        print(wozek)
        cursor = conn.cursor()

        sql_object = sql.SQL(f"SELECT * FROM \"Dzial\" WHERE id = {wozek[1]} LIMIT 1")

        try:
            cursor.execute(sql_object)
            dzial = cursor.fetchall()
        except Exception as e:
            print ("ERROR w get_wozki:", e)
            conn.rollback()
            dzial = []
        finally:
            cursor.close()
        print(dzial)
        cursor = conn.cursor()

        sql_object = sql.SQL(f"SELECT * FROM \"Magazyn\" WHERE id = {dzial[0][1]} LIMIT 1")

        try:
            cursor.execute(sql_object)
            mag = cursor.fetchall()
        except Exception as e:
            print ("ERROR w get_wozki:", e)
            conn.rollback()
            mag = []
        finally:
            cursor.close()
        print(mag)
        print("!!!",wozek, dzial, mag, "!!!!")
        new_wozki.append((mag[0][1], dzial[0][2], wozek[3], wozek[2]))

    return new_wozki    

def dodaj_transakcje(conn, data, klient):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Klient\" WHERE nazwa = \'{klient}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_transakcje: znajdz_id magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Transakcja\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w stworz_transakcje: znajdz_id dla dzialu: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"INSERT INTO \"Transakcja\" VALUES (\'{current_id}\', \'{mag_id}\', \'{data}\')")
    
    try:
        cursor.execute(sql_object)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_tansakcje: dodawanie do bazy: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_wszystkietransakcje(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL("SELECT * FROM \"Transakcja\"")

    try:
        cursor.execute(sql_object)
        transakcje = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_klienci:", e)
        conn.rollback()
        transakcje = []
    finally:
        cursor.close()

    klienci =  {}
    
    for trans in transakcje:
        cursor = conn.cursor()

        sql_object = sql.SQL(f"SELECT nazwa FROM \"Klient\" WHERE id = {trans[1]} LIMIT 1")

        try:
            cursor.execute(sql_object)
            nazwa_klienta = cursor.fetchone()[0]
        except Exception as e:
            print ("ERROR w nazwie magazynu:", e)
            conn.rollback()
            nazwa_klienta = ""
        finally:
            cursor.close()
        klienci[trans[1]] = nazwa_klienta

    return transakcje, klienci

def get_polki(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL(''' SELECT * FROM polki ''')

    try:
        cursor.execute(sql_object)
        transakcje = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_polki:", e)
        conn.rollback()
        transakcje = []
    finally:
        cursor.close()

    return transakcje

def stworz_przedmiot(conn, Mag, Dzial, Regal, Polka, Nazwa, Cena, Ilosc):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT * FROM \"Magazyn\" WHERE nazwa = \'{Mag}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    nowydzial = False

    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Dzial\" WHERE nazwa = \'{Dzial}\' AND id_magazyn = {mag_id} LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        dzial_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke dla dzialu: ", e)
        conn.rollback()
        try:
            stworz_dzial(conn, Dzial, Mag)
            print("Stworzono nowy dzial:", Mag, Dzial)
            nowydzial = True
        except Exception as e:
            print("Blad w tworzeniu nowego dzialu:", e)
    finally:
        cursor.close()

    if nowydzial:
        cursor = conn.cursor()
        find_id = sql.SQL(f"SELECT * FROM \"Dzial\" WHERE nazwa = \'{Dzial}\' AND id_magazyn = {mag_id} LIMIT 1")
        try:
            cursor.execute(find_id)
            conn.commit()
            dzial_id = int(cursor.fetchone()[0])
        except Exception as e:
            print ("ERROR w stworz_dzial: stworz_polke dla dzialu: ", e)
            conn.rollback()
            return False
        finally:
            cursor.close()

    ###########
    nowepolozenie = False

    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Polozenie\" WHERE regal = {Regal} AND polka = {Polka} AND id_dzial = {dzial_id} LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        polozenie_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_polke dla dzialu: ", e)
        conn.rollback()
        try:
            stworz_polke(conn, Mag, Dzial, Regal, Polka)
            print("Stworzono nowa polke:", Mag, Dzial, Regal, Polka)
            nowepolozenie = True
        except Exception as e:
            print("Blad w tworzeniu nowej polki:", e)
    finally:
        cursor.close()

    if nowepolozenie:
        cursor = conn.cursor()
        find_id = sql.SQL(f"SELECT * FROM \"Polozenie\" WHERE regal = {Regal} AND polka = {Polka} AND id_dzial = {dzial_id} LIMIT 1")
        try:
            cursor.execute(find_id)
            conn.commit()
            polozenie_id = int(cursor.fetchone()[0])
        except Exception as e:
            print ("ERROR w stworz_dzial: stworz_polke dla dzialu: ", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
    ###########
    cursor = conn.cursor()
    find_id = sql.SQL(f"SELECT * FROM \"Przedmiot\" ORDER BY id DESC LIMIT 1")
    try:
        cursor.execute(find_id)
        conn.commit()
        current_id = int(cursor.fetchone()[0]) + 1
    except Exception as e:
        print ("ERROR w stworz_przedmiot: stworz_przedmiot dla Przedmiot: ", e)
        conn.rollback()
        current_id = 1
    finally:
        cursor.close()

    cursor = conn.cursor()
    sql_object = sql.SQL(f"SELECT * FROM \"Przedmiot\"  WHERE id_poloz = {polozenie_id} AND nazwa = \'{Nazwa}\' AND cena = {Cena}")
    nowailosc = 0
    Niemaprzedmiotu = False
    try:
        cursor.execute(sql_object)
        conn.commit()
        nowailosc = int(cursor.fetchone()[5]) + int(Ilosc)
    except Exception as e:
        print ("NIE MA TAKIEGO PRZEDMIOTU (JESZCZE): ", e)
        Niemaprzedmiotu = True
        conn.rollback()
    finally:
        cursor.close()

    if Niemaprzedmiotu:
        cursor = conn.cursor()
        sql_object = sql.SQL(f"INSERT INTO \"Przedmiot\" (id, id_poloz, nazwa, cena, ilosc) VALUES (\'{current_id}\', {polozenie_id}, \'{Nazwa}\', {Cena}, {Ilosc})")
        
        try:
            cursor.execute(sql_object)
            conn.commit()
        except Exception as e:
            print ("ERROR w stworz_dzial: stworz_polke dodawanie do bazy: ", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
    else:
        cursor = conn.cursor()
        sql_object = sql.SQL(f"UPDATE \"Przedmiot\" SET ilosc = {nowailosc} WHERE id_poloz = {polozenie_id}  AND nazwa = \'{Nazwa}\' AND cena = {Cena}")
        
        try:
            cursor.execute(sql_object)
            conn.commit()
        except Exception as e:
            print ("ERROR w updatowaniu przedmiotu: ", e)
            conn.rollback()
            return False
        finally:
            cursor.close()

def get_przedmioty(conn):
    cursor = conn.cursor()

    sql_object = sql.SQL(''' SELECT \"Magazyn\".nazwa,
     \"Dzial\".nazwa, \"Polozenie\".regal, \"Polozenie\".polka, 
     \"Przedmiot\".nazwa, \"Przedmiot\".ilosc, \"Przedmiot\".cena
     FROM \"Polozenie\"
     JOIN \"Dzial\" ON id_dzial = \"Dzial\".id 
     JOIN \"Magazyn\" ON \"Dzial\".id_magazyn = \"Magazyn\".id
     JOIN \"Przedmiot\" ON \"Przedmiot\".id_poloz = \"Polozenie\".id ''')

    try:
        cursor.execute(sql_object)
        transakcje = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_polki:", e)
        conn.rollback()
        transakcje = []
    finally:
        cursor.close()

    return transakcje

def stworz_dzialosoba(conn, id_osoba, dzial):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT id_mag FROM \"Pracownik\" WHERE id = {id_osoba} LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mag_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba magazynu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
    
    czydzial = False

    cursor = conn.cursor()
    qmag_id = sql.SQL(f"SELECT id FROM \"Dzial\" WHERE id_magazyn = {mag_id} AND nazwa = \'{dzial}\' LIMIT 1")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        dzial_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
        conn.rollback()
        czydzial = True
    finally:
        cursor.close()

    if czydzial:
        cursor = conn.cursor()
        qmag_id = sql.SQL(f"SELECT nazwa FROM \"Magazyn\" WHERE id = {mag_id} LIMIT 1")
        try:
            cursor.execute(qmag_id)
            conn.commit()
            magnazwa = int(cursor.fetchone()[0])
        except Exception as e:
            print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
            conn.rollback()
            czydzial = True
        finally:
            cursor.close()

        try:
            stworz_dzial(conn, dzial, magnazwa)
        except Exception as e:
            print("Dzialosoba stworz_dzial: ", e) 
        
        cursor = conn.cursor()
        qmag_id = sql.SQL(f"SELECT id FROM \"Dzial\" WHERE id_magazyn = {mag_id} AND nazwa = \'{dzial}\' LIMIT 1")
        try:
            cursor.execute(qmag_id)
            conn.commit()
            dzial_id = int(cursor.fetchone()[0])
        except Exception as e:
            print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
            conn.rollback()
            czydzial = True
        finally:
            cursor.close()
    
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"INSERT INTO \"Dzial_Osoba\" VALUES ({id_osoba}, {dzial_id})")
    try:
        cursor.execute(qmag_id)
        conn.commit()
        dzial_id = int(cursor.fetchone()[0])
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
        conn.rollback()
        czydzial = True
    finally:
        cursor.close()

def get_dzialosoby(conn):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f'SELECT * from dzialosoba')
    try:
        cursor.execute(qmag_id)
        conn.commit()
        dzialosoba = cursor.fetchall()
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    return dzialosoba

def stworz_przedtrans(conn, przedmiot_id, trans_id, ilosc):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f'SELECT * from \"Przedmiot\" WHERE id = {przedmiot_id}')
    try:
        cursor.execute(qmag_id)
        conn.commit()
        przedmiotilosc = int(cursor.fetchone()[4])
    except Exception as e:
        print ("ERROR w SELECT stworz_przedtrans: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    if przedmiotilosc < int(ilosc):
        return True
    
    cursor = conn.cursor()
    qmag_id = sql.SQL(f"INSERT INTO \"Przed_trans\" VALUES ({przedmiot_id}, {trans_id})")
    try:
        cursor.execute(qmag_id)
        conn.commit()
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
        conn.rollback()
    finally:
        cursor.close()

    cursor = conn.cursor()
    qmag_id = sql.SQL(f"UPDATE \"Przedmiot\" SET ilosc = ilosc - {ilosc} WHERE id = {przedmiot_id}")
    try:
        cursor.execute(qmag_id)
        conn.commit()
    except Exception as e:
        print ("ERROR w UPDATE przedtrans: ", e)
        conn.rollback()
    finally:
        cursor.close()

    return False

def get_tylkoprzedmioty(conn):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f'SELECT * from \"Przedmiot\"')
    try:
        cursor.execute(qmag_id)
        conn.commit()
        dzialosoba = cursor.fetchall()
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    return dzialosoba

def get_przedtrans(conn):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f'SELECT * from przedtrans')
    try:
        cursor.execute(qmag_id)
        conn.commit()
        dzialosoba = cursor.fetchall()
    except Exception as e:
        print ("ERROR w stworz_dzial: stworz_dzialosoba dzialu: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()

    return dzialosoba

def get_ilepracownikow(conn):
    cursor = conn.cursor()
    qmag_id = sql.SQL(f'SELECT id, nazwa from "Magazyn"')
    try:
        cursor.execute(qmag_id)
        conn.commit()
        mags = cursor.fetchall()
    except Exception as e:
        print ("ERROR w get_ilepracownikow: ", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
    ilosc = {}
    for magid in mags:
        print("TESTESTEST: ", magid[0])
        cursor = conn.cursor()
        qmag_id = sql.SQL(f'SELECT Count(*) from "Pracownik" WHERE id_mag={magid[0]}')
        try:
            cursor.execute(qmag_id)
            conn.commit()
            il = int(cursor.fetchone()[0])
            print("IL: ", il)
            ilosc[magid[1]] = il
        except Exception as e:
            print ("ERROR w get_ilepracownikow: ", e)
            conn.rollback()
            return False
        finally:
            cursor.close()

    return ilosc
