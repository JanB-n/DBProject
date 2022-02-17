CREATE TABLE "Magazyn" (
  "id" SERIAL PRIMARY KEY,
  "nazwa" varchar,
  "kraj" varchar,
  "miasto" varchar,
  "ulica" varchar,
  "numer" varchar,
  "kod" varchar
);

CREATE TABLE "Dzial" (
  "id" int PRIMARY KEY,
  "id_magazyn" int,
  "nazwa" varchar
);

CREATE TABLE "Przedmiot" (
  "id" int PRIMARY KEY,
  "id_poloz" int,
  "nazwa" varchar,
  "cena" decimal,
  "ilosc" int
);

CREATE TABLE "Polozenie" (
  "id" int PRIMARY KEY,
  "regal" int,
  "polka" int,
  "id_dzial" int
);

CREATE TABLE "Przed_trans" (
  "id_przed" int,
  "id_trans" int
);

CREATE TABLE "Klient" (
  "id" int PRIMARY KEY,
  "nazwa" varchar,
  "NIP" varchar,
  "REGON" varchar,
  "adres" varchar,
  "typ" varchar,
  "telefon" int
);

CREATE TABLE "Transakcja" (
  "id" int PRIMARY KEY,
  "id_klient" int,
  "data" date
);

CREATE TABLE "Wozek" (
  "id" int PRIMARY KEY,
  "id_dzial" int,
  "nosnosc" int,
  "producent" varchar
);

CREATE TABLE "Pracownik" (
  "id" int PRIMARY KEY,
  "id_mag" int,
  "rola" int,
  "imie" varchar,
  "nazwisko" varchar
);

CREATE TABLE "Dzial_Osoba" (
  "id_pracownik" int,
  "id_dzial" int
);

ALTER TABLE "Dzial" ADD FOREIGN KEY ("id_magazyn") REFERENCES "Magazyn" ("id");

ALTER TABLE "Polozenie" ADD FOREIGN KEY ("id_dzial") REFERENCES "Dzial" ("id");

ALTER TABLE "Przedmiot" ADD FOREIGN KEY ("id_poloz") REFERENCES "Polozenie" ("id");

ALTER TABLE "Pracownik" ADD FOREIGN KEY ("id_mag") REFERENCES "Magazyn" ("id");

ALTER TABLE "Dzial_Osoba" ADD FOREIGN KEY ("id_pracownik") REFERENCES "Pracownik" ("id");

ALTER TABLE "Dzial_Osoba" ADD FOREIGN KEY ("id_dzial") REFERENCES "Dzial" ("id");

ALTER TABLE "Przed_trans" ADD FOREIGN KEY ("id_trans") REFERENCES "Transakcja" ("id");

ALTER TABLE "Przed_trans" ADD FOREIGN KEY ("id_przed") REFERENCES "Przedmiot" ("id");

ALTER TABLE "Transakcja" ADD FOREIGN KEY ("id_klient") REFERENCES "Klient" ("id");

ALTER TABLE "Wozek" ADD FOREIGN KEY ("id_dzial") REFERENCES "Dzial" ("id");
