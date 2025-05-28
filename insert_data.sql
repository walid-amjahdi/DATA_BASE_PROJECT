-- Données pour Hotel
INSERT INTO Hotel (id_hotel, ville, pays, code_postal) VALUES
(1, 'Paris', 'France', '75001'),
(2, 'Lyon', 'France', '69002');

-- Données pour Client
INSERT INTO Client (id_client, nom_complet, adresse, ville, code_postal, email, tel) VALUES
(1, 'Jean Dupont', '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678'),
(2, 'Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789'),
(3, 'Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890'),
(4, 'Lucie Martin', '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901'),
(5, 'Emma Giraud', '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012');

-- Données pour Prestation
INSERT INTO Prestation (id_prestation, libelle, prix) VALUES
(1, 'Petit-déjeuner', 15),
(2, 'Navette aéroport', 30),
(3, 'Wi-Fi gratuit', 0),
(4, 'Spa et bien-être', 50),
(5, 'Parking sécurisé', 20);

-- Données pour TypeChambre
INSERT INTO TypeChambre (id_type, libelle, tarif) VALUES
(1, 'Simple', 80),
(2, 'Double', 120);

-- Données pour Chambre
INSERT INTO Chambre (id_chambre, etage, fumeurs, id_hotel, id_type) VALUES
(1, 2, 0, 1, 1),
(2, 5, 1, 1, 2),
(3, 3, 0, 2, 1),
(4, 4, 0, 2, 2),
(5, 1, 1, 2, 2),
(6, 2, 0, 1, 1),
(7, 3, 1, 1, 2),
(8, 1, 0, 1, 1);

-- Données pour Reservation
INSERT INTO Reservation (id_reservation, date_arrivee, date_depart, id_client) VALUES
(1, '2025-06-15', '2025-06-18', 1),
(2, '2025-07-01', '2025-07-05', 2),
(3, '2025-08-10', '2025-08-14', 3),
(4, '2025-09-05', '2025-09-07', 4),
(5, '2025-09-20', '2025-09-25', 5),
(7, '2025-11-12', '2025-11-14', 2),
(9, '2026-01-15', '2026-01-18', 4),
(10, '2026-02-01', '2026-02-05', 2);

-- Données pour Evaluation
INSERT INTO Evaluation (id_evaluation, date_eval, note, commentaire, id_reservation) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);
