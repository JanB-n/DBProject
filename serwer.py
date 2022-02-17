import urllib.parse as up
import psycopg2
from funkcje import *
from flask import Flask, render_template, request, flash
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse, abort


try:
    up.uses_netloc.append("postgres")
    url = up.urlparse("postgres://ikmnmrdc:sON_cd4bgYLiNrXFufBhX7_9iEKCtn3Z@ella.db.elephantsql.com/ikmnmrdc")
    conn = psycopg2.connect(database=url.path[1:],
                            user=url.username,
                            password=url.password,
                            host=url.hostname,
                            port=url.port)
except Exception as ex:
    print("BLAD POLACZENIA Z BAZA DANYCH")
    print(ex)

app = Flask(__name__, template_folder='./templates')
CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = "sekretnyklucz"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/magazyn', methods=['GET'])
def gmagazyn():
    return render_template('magazyn.html')

@app.route('/magazyn', methods=['POST'])
def magazyn():
    Nazwa = request.form.get('nazwa')
    Kraj = request.form.get('kraj')
    Miasto = request.form.get('miasto')
    Ulica = request.form.get('ulica')
    Numer = request.form.get('numer')
    Kod = request.form.get('kod')
    print("DANE: ",Nazwa, Kraj, Miasto, Ulica, Numer, Kod)
    try:
        stworz_magazyn(conn, Nazwa, Kraj, Miasto, Ulica, Numer, Kod)
        flash('Magazyn zostal utworzony')
    except Exception as ex:
        flash('Nie udalo sie utworzyc magazynu')
        print(ex)
    return render_template('magazyn.html')

@app.route('/magazyny')
def magazyny():
    try:
        mags = get_magazyny(conn)
        print(mags)
    except Exception as ex:
        print(ex)
    return render_template('magazyny.html', mags = mags)

@app.route('/pracownik', methods=['GET'])
def gpracownik():
    try:
        mags = get_magazyny(conn)
    except Exception as ex:
        print(ex)
    return render_template('pracownik.html', mags=mags)

@app.route('/pracownik', methods=['POST'])
def pracownik():
    imie = request.form.get('imie')
    nazwisko = request.form.get('nazwisko')
    rola = request.form.get('rola')
    Mag = request.form.get('wybranymag')
    try:
        stworz_pracownik(conn, imie, nazwisko, rola, Mag)
    except Exception as ex:
        print(ex)
    try:
        mags = get_magazyny(conn)
    except Exception as ex:
        print(ex)
    return render_template('pracownik.html', mags=mags)

@app.route('/pracownicy')
def pracownicy():
    try:
        pracownicy, magazyny = get_wszyscypracownicy(conn)
        iloscpracownikow = get_ilepracownikow(conn)
        inv_mags = {}
        for k, v in magazyny.items():
            inv_mags[v] = magazyny.get(v, []) + [k]
        print("PRACOWNICY: ", pracownicy, inv_mags)
        print("Ilosci pracownikow: ", iloscpracownikow)
    except Exception as ex:
        print(ex)
    return render_template('pracownicy.html', pracownicy=pracownicy, mags=inv_mags, ilosc=iloscpracownikow)

@app.route('/dzial', methods=['GET'])
def gdzial():
    try:
        mags = get_magazyny(conn)
    except Exception as ex:
        print(ex)
    return render_template('dzial.html', mags=mags)

@app.route('/dzial', methods=['POST'])
def dzial():
    Nazwa = request.form.get('nazwadzialu')
    Mag = request.form.get('wybranymag')
    print("dzial: ", Nazwa, Mag)
    try:
        stworz_dzial(conn, Nazwa, Mag)
    except Exception as ex:
        print(ex)
    try:
        mags = get_magazyny(conn)
    except Exception as ex:
        print(ex)
    return render_template('dzial.html', mags=mags)

@app.route('/dzialy', methods=['GET'])
def dzialy():
    try:
        dzialy, magazyny = get_wszystkiedzialy(conn)
        inv_mags = {}
        for k, v in magazyny.items():
            inv_mags[v] = magazyny.get(v, []) + [k]
        print("DZIALY: ", dzialy, inv_mags)
    except Exception as ex:
        print(ex)
    return render_template('dzialy.html', dzialy=dzialy, mags=inv_mags)

@app.route('/polka', methods=['GET'])
def gpolka():
    try:
        mags = get_magazyny(conn)
        dzialy = get_dzialyall(conn)
        print('POLKA', mags, dzialy)
    except Exception as ex:
        print(ex)
    return render_template('polka.html', mags=mags, dzialy=dzialy)

@app.route('/polka', methods=['POST'])
def polka():
    Regal = request.form.get('regal')
    Polka = request.form.get('polka')
    Mag = request.form.get('wybranymag')
    Dzial = request.form.get('wybranydzial')
    print("Polka: ", Mag, Dzial, Regal, Polka)
    try:
        stworz_polke(conn, Mag, Dzial, Regal, Polka)
    except Exception as ex:
        print(ex)
    try:
        mags = get_magazyny(conn)
        dzialy = get_dzialyall(conn)
    except Exception as ex:
        print(ex)
    return render_template('polka.html', mags=mags, dzialy=dzialy)

@app.route('/polki', methods=['GET'])
def polki():
    try:
        polki = get_polki(conn)
        print("DZIALY: ", polki)
    except Exception as ex:
        print(ex)
    return render_template('polki.html', polki = polki)

@app.route('/przedmiot', methods=['POST'])
def przedmiot():
    Polka = request.form.get('wybranapolka')
    Regal = request.form.get('wybranyregal')
    Mag = request.form.get('wybranymag')
    Dzial = request.form.get('wybranydzial')
    Cena = request.form.get('cena')
    Nazwa = request.form.get('nazwa')
    Ilosc = request.form.get('ilosc')
    print("Przedmiot: ", Mag, Dzial, Regal, Polka, Nazwa, Cena, Ilosc)
    try:
        stworz_przedmiot(conn, Mag, Dzial, Regal, Polka, Nazwa, Cena, Ilosc)
    except Exception as ex:
        print(ex)
    try:
        mags = get_magazyny(conn)
        dzialy = get_dzialyall(conn)
        polki = get_polki(conn)
        print('POLKA', mags, dzialy, polki)
    except Exception as ex:
        print(ex)
    return render_template('przedmiot.html', mags=mags, dzialy=dzialy, polki=polki)

@app.route('/przedmiot', methods=['GET'])
def gprzedmiot():
    try:
        mags = get_magazyny(conn)
        dzialy = get_dzialyall(conn)
        polki = get_polki(conn)
        print('POLKA', mags, dzialy, polki)
    except Exception as ex:
        print(ex)
    return render_template('przedmiot.html', mags=mags, dzialy=dzialy, polki=polki)

@app.route('/przedmioty', methods=['GET'])
def przedmioty():
    try:
        przedmioty = get_przedmioty(conn)
        print("Przedmioty: ", przedmioty)
    except Exception as ex:
        print(ex)
    return render_template('przedmioty.html', przedmioty=przedmioty)

@app.route('/transakcja', methods=['GET'])
def gtransakcja():
    try:
        klienci = get_klienci(conn)
    except Exception as ex:
        print(ex)
    return render_template('transakcja.html', klienci=klienci)

@app.route('/transakcja', methods=['POST'])
def transakcja():
    try:
        klienci = get_klienci(conn)
    except Exception as ex:
        print(ex)

    data = request.form.get('data')
    klient = request.form.get('wybranyklient')
    try:
        dodaj_transakcje(conn, data, klient)
        flash('Transakcja zostala dodany')
    except Exception as ex:
        flash('Nie udalo sie dodac transakcji')
        print(ex)
    return render_template('transakcja.html', klienci=klienci)

@app.route('/transakcje', methods=['GET'])
def transakcje():
    try:
        transakcje, klienci = get_wszystkietransakcje(conn)
        inv_mags = {}
        for k, v in klienci.items():
            inv_mags[v] = klienci.get(v, []) + [k]
        print("DZIALY: ", transakcje, inv_mags)
    except Exception as ex:
        print(ex)
    return render_template('transakcje.html', trans=transakcje, klienci=inv_mags)
    

@app.route('/klient', methods=['GET'])
def gklienci():
    return render_template('klienci.html')

@app.route('/klient', methods=['POST'])
def klienci():
    nazwa = request.form.get('nazwa')
    NIP = request.form.get('nip')
    REGON = request.form.get('regon')
    adres = request.form.get('adres')
    typ = request.form.get('typ')
    telefon = request.form.get('telefon')
    try:
        stworz_klienta(conn, nazwa, NIP, REGON, adres, typ, telefon)
        flash('Klient zostal dodany')
    except Exception as ex:
        flash('Nie udalo sie dodac wozka')
        print(ex)
    return render_template('klienci.html')

@app.route('/klienci', methods=['GET'])
def pokazklienci():
    try:
        klienci = get_klienci(conn)
    except Exception as ex:
        print(ex)
    return render_template('pokazklienci.html', klienci=klienci)

@app.route('/wozek', methods=['GET'])
def gwozek():
    try:
        dzialy, magazyny = get_wszystkiedzialy(conn)
        inv_mags = {}
        for k, v in magazyny.items():
            inv_mags[v] = magazyny.get(v, []) + [k]
        print("DZIALY: ", dzialy, inv_mags)
    except Exception as ex:
        print(ex)
    return render_template('wozek.html', dzialy=dzialy, mags=inv_mags)

@app.route('/wozek', methods=['POST'])
def wozek():
    try:
        dzialy, magazyny = get_wszystkiedzialy(conn)
        inv_mags = {}
        for k, v in magazyny.items():
            inv_mags[v] = magazyny.get(v, []) + [k]
        print("DZIALY: ", dzialy, inv_mags)
    except Exception as ex:
        print(ex)
    id = request.form.get('id')
    producent = request.form.get('producent')
    nosnosc = request.form.get('nosnosc')
    try:
        dodaj_wozek(conn, id, producent, nosnosc)
        flash('Wozek zostal dodany')
    except Exception as ex:
        flash('Nie udalo sie dodac wozka')
        print(ex)

    return render_template('wozek.html', dzialy=dzialy, mags=inv_mags)

@app.route('/wozki')
def wozki():
    try:
        wozki = get_wozki(conn)
        print("WOZKI:", wozki)
    except Exception as ex:
        print(ex)
    return render_template('wozki.html', wozki = wozki)

@app.route('/dzialosoba', methods=['GET'])
def gdzialosoba():
    try:
        osoby = get_osoby(conn)
        dzialy = get_dzialyall(conn)
        print("Osoby i dzialy:", osoby, dzialy)
    except Exception as ex:
        print(ex)
    return render_template('dzialosoba.html', osoby=osoby, dzialy=dzialy)

@app.route('/dzialosoba', methods=['POST'])
def dzialosoba():
    id_osoba = request.form.get('wybranaosoba')
    dzial = request.form.get('wybranydzial')
    try:
        stworz_dzialosoba(conn, id_osoba, dzial)
    except Exception as e:
        print(e)
    try:
        osoby = get_osoby(conn)
        dzialy = get_dzialyall(conn)
        print("Osoby i dzialy:", osoby, dzialy)
    except Exception as ex:
        print(ex)
    return render_template('dzialosoba.html', osoby=osoby, dzialy=dzialy)

@app.route('/dzialosoby', methods=['GET'])
def dzialosoby():
    try:
        dzialosoby = get_dzialosoby(conn)
        print("WOZKI:", dzialosoby)
    except Exception as ex:
        print(ex)
    return render_template('dzialosoby.html', dzialosoby=dzialosoby)

@app.route('/przedtrans', methods=['GET'])
def gprzedtrans():
    try:
        przedmioty = get_tylkoprzedmioty(conn)
        transakcje, klienci = get_wszystkietransakcje(conn)
        print(transakcje, klienci)
        print("Przedmioty:", przedmioty)
        print("Transakcje:", transakcje)
        print("Klienci:", klienci)
        zaduzo=False
    except Exception as ex:
        print(ex)
    return render_template('przedtrans.html', przedmioty=przedmioty, transakcje=transakcje, klienci=klienci, zaduzo=zaduzo)

@app.route('/przedtrans', methods=['POST'])
def przedtrans():
    przedmiot_id = request.form.get('wybranyprzedmiot')
    trans_id = request.form.get('wybranatransakcja')
    ilosc = request.form.get('ilosc')
    print("POST przedtrans: ", przedmiot_id, trans_id, ilosc)
    try:
        zaduzo = stworz_przedtrans(conn, przedmiot_id, trans_id, ilosc)
    except Exception as e:
        print(e)

    try:
        przedmioty = get_tylkoprzedmioty(conn)
        transakcje, klienci = get_wszystkietransakcje(conn)
        print(transakcje, klienci)
        print("Transakcje:", transakcje)
        print("Klienci:", klienci)
    except Exception as ex:
        print(ex)
    return render_template('przedtrans.html', przedmioty=przedmioty, transakcje=transakcje, klienci=klienci, zaduzo=zaduzo)

@app.route('/przedtransakcji', methods=['GET'])
def przedtransakcji():
    try:
        przedtrans = get_przedtrans(conn)
        print("WOZKI:", przedtrans)
    except Exception as ex:
        print(ex)
    return render_template('przedtransakcji.html', przedtrans=przedtrans)

if __name__ == "__main__":
    app.run(debug=True)

