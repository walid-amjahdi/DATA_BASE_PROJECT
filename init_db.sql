-- ==================== BASE ====================
-- Note : SQLite ne gère pas CREATE DATABASE ou USE


-- Suppression des tables si elles existent déjà (pour re-créer proprement)

DROP TABLE IF EXISTS Hotel_Prestation;
DROP TABLE IF EXISTS Reservation_Chambre;
DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS Prestation;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Chambre;
DROP TABLE IF EXISTS TypeChambre;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Hotel;



-- =================== ENTITÉS ===================
CREATE TABLE Hotel (
  id_hotel INTEGER PRIMARY KEY AUTOINCREMENT,
  ville TEXT,
  pays TEXT,
  code_postal TEXT
);

CREATE TABLE TypeChambre (
  id_type INTEGER PRIMARY KEY AUTOINCREMENT,
  libelle TEXT,
  tarif REAL
);

CREATE TABLE Chambre (
  id_chambre INTEGER PRIMARY KEY AUTOINCREMENT,
  etage INTEGER,
  fumeurs BOOLEAN,
  id_hotel INTEGER,
  id_type INTEGER,
  FOREIGN KEY(id_hotel) REFERENCES Hotel(id_hotel),
  FOREIGN KEY(id_type) REFERENCES TypeChambre(id_type)
);

CREATE TABLE Client (
  id_client INTEGER PRIMARY KEY AUTOINCREMENT,
  nom_complet TEXT,
  adresse TEXT,
  ville TEXT,
  code_postal TEXT,
  email TEXT,
  tel TEXT
);

CREATE TABLE Reservation (
  id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
  date_arrivee TEXT,   -- SQLite n’a pas de type DATE natif
  date_depart TEXT,
  id_client INTEGER,
  FOREIGN KEY(id_client) REFERENCES Client(id_client)
);

CREATE TABLE Prestation (
  id_prestation INTEGER PRIMARY KEY AUTOINCREMENT,
  libelle TEXT,
  prix REAL
);

CREATE TABLE Evaluation (
  id_evaluation INTEGER PRIMARY KEY AUTOINCREMENT,
  date_eval TEXT,
  note INTEGER,
  commentaire TEXT,
  id_reservation INTEGER,
  FOREIGN KEY(id_reservation) REFERENCES Reservation(id_reservation)
);

-- ============ ASSOCIATIONS M‑N ============

CREATE TABLE Reservation_Chambre (
  id_reservation INTEGER,
  id_chambre INTEGER,
  PRIMARY KEY(id_reservation, id_chambre),
  FOREIGN KEY(id_reservation) REFERENCES Reservation(id_reservation),
  FOREIGN KEY(id_chambre) REFERENCES Chambre(id_chambre)
);

CREATE TABLE Hotel_Prestation (
  id_hotel INTEGER,
  id_prestation INTEGER,
  PRIMARY KEY(id_hotel, id_prestation),
  FOREIGN KEY(id_hotel) REFERENCES Hotel(id_hotel),
  FOREIGN KEY(id_prestation) REFERENCES Prestation(id_prestation)
);
