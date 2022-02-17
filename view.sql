CREATE VIEW dzialosoba AS SELECT "Pracownik".imie, "Pracownik".nazwisko, 
"Dzial".nazwa FROM "Dzial_Osoba"
JOIN "Pracownik" ON "Dzial_Osoba".id_pracownik = "Pracownik".id
JOIN "Dzial" ON "Dzial".id = "Dzial_Osoba".id_dzial;

---------------------

CREATE VIEW przedtrans AS SELECT "Przedmiot".nazwa AS pnazwa, "Transakcja".data, 
"Klient".nazwa AS knazwa FROM "Przed_trans"
JOIN "Przedmiot" ON "Przed_trans".id_przed = "Przedmiot".id
JOIN "Transakcja" ON "Transakcja".id = "Przed_trans".id_trans
JOIN "Klient" ON "Klient".id = "Transakcja".id_klient;

---------------------

CREATE VIEW polki AS SELECT "Magazyn".nazwa AS mnazwa,
"Dzial".nazwa AS dnazwa, "Polozenie".regal, "Polozenie".polka FROM "Polozenie"
JOIN "Dzial" ON id_dzial = "Dzial".id 
JOIN "Magazyn" ON "Dzial".id_magazyn = "Magazyn".id