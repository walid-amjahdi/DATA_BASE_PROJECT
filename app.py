import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
import uuid
import re

# Page configuration
st.set_page_config(page_title="Nexus Hotel - Gestion", layout="wide")

# Custom CSS for improved UI
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #1a73e8;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stSubheader {
            color: #444;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .stButton>button {
            background-color: #1a73e8 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5em 1em !important;
            font-size: 1rem !important;
            transition: background-color 0.3s ease !important;
        }
        .stButton>button:hover {
            background-color: #0c59cf !important;
        }
        .stTextInput>div>div>input,
        .stDateInput>div>input {
            border-radius: 6px;
            padding: 8px;
            border: 1px solid #ccc;
        }
        .stDataFrame {
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Voir les réservations"

def get_db_connection():
    conn = sqlite3.connect("db.sqlite", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def render_navigation():
    st.title("Nexus Hotel - Système de Gestion")
    cols = st.columns(5)
    labels = [
        "Voir les réservations",
        "Voir les clients",
        "Ajouter un client",
        "Ajouter une réservation",
        "Voir les chambres disponibles"
    ]
    for i, label in enumerate(labels):
        if cols[i].button(label, key=f"nav_{i}"):
            st.session_state.page = label

def view_reservations():
    st.subheader("Liste des réservations")
    with st.spinner("Chargement des réservations..."):
        with get_db_connection() as conn:
            query = """
            SELECT r.id_reservation, r.date_arrivee, r.date_depart,
                   c.nom_complet AS client, 
                   COALESCE(h.ville, 'No Hotel Assigned') AS hotel
            FROM Reservation r
            JOIN Client c ON c.id_client = r.id_client
            LEFT JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
            LEFT JOIN Chambre ch ON rc.id_chambre = ch.id_chambre
            LEFT JOIN Hotel h ON ch.id_hotel = h.id_hotel
            ORDER BY r.date_arrivee DESC
            """
            df = pd.read_sql_query(query, conn)

    col1, col2 = st.columns([2, 1])
    with col1:
        date_filter = st.date_input("Filtrer à partir de", min_value=date.today())
    with col2:
        if st.button("Filtrer"):
            df = df[pd.to_datetime(df['date_arrivee']) >= pd.to_datetime(date_filter)]

    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("Supprimer une réservation"):
        with get_db_connection() as conn:
            res_ids = conn.execute("SELECT id_reservation FROM Reservation ORDER BY id_reservation DESC").fetchall()
            latest_id = res_ids[0]['id_reservation'] if res_ids else 0

        reservation_id = st.number_input("ID de la réservation à supprimer", min_value=1, max_value=latest_id, step=1)
        confirm_delete = st.checkbox("Confirmer la suppression")
        
        if st.button("Supprimer"):
            if not confirm_delete:
                st.error("❌ Veuillez confirmer la suppression.")
            else:
                with st.spinner("Suppression en cours..."):
                    with get_db_connection() as conn:
                        cur = conn.cursor()
                        cur.execute("SELECT id_reservation FROM Reservation WHERE id_reservation = ?", (reservation_id,))
                        if not cur.fetchone():
                            st.error("❌ Réservation non trouvée.")
                        else:
                            # Delete from all related tables
                            cur.execute("DELETE FROM Evaluation WHERE id_reservation = ?", (reservation_id,))
                            cur.execute("DELETE FROM Reservation_Chambre WHERE id_reservation = ?", (reservation_id,))
                            cur.execute("DELETE FROM Reservation WHERE id_reservation = ?", (reservation_id,))
                            conn.commit()
                            st.success("✅ Réservation supprimée avec succès")
                            st.rerun()

def view_clients():
    st.subheader("Liste des clients")
    with st.spinner("Chargement des clients..."):
        with get_db_connection() as conn:
            df = pd.read_sql_query("""
                SELECT id_client, nom_complet, adresse, ville, code_postal, email, tel 
                FROM Client 
                ORDER BY nom_complet
                """, conn)

    search_term = st.text_input("Rechercher un client (nom ou email)")
    if search_term:
        df = df[df['nom_complet'].str.contains(search_term, case=False, na=False) | 
                df['email'].str.contains(search_term, case=False, na=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)

def add_client():
    st.subheader("Ajouter un nouveau client")
    st.markdown("**Tous les champs sont obligatoires.**")
    
    with st.form("form_client"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet *")
            email = st.text_input("Email *")
            tel = st.text_input("Téléphone *")
        with col2:
            adresse = st.text_input("Adresse *")
            ville = st.text_input("Ville *")
            code_postal = st.text_input("Code postal *")

        submit = st.form_submit_button("Ajouter")

    if submit:
        missing_fields = []
        if not nom.strip(): missing_fields.append("Nom complet")
        if not email.strip(): missing_fields.append("Email")
        if not tel.strip(): missing_fields.append("Téléphone")
        if not adresse.strip(): missing_fields.append("Adresse")
        if not ville.strip(): missing_fields.append("Ville")
        if not code_postal.strip(): missing_fields.append("Code postal")

        if missing_fields:
            st.error(f"❌ Veuillez remplir tous les champs obligatoires : {', '.join(missing_fields)}")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("❌ Format d'email invalide.")
        elif not re.match(r"^\+?\d{9,}$", tel.replace(' ', '')):
            st.error("❌ Format de téléphone invalide (au moins 9 chiffres).")
        elif not re.match(r"^\d{5}$", code_postal.strip()):
            st.error("❌ Le code postal doit contenir exactement 5 chiffres.")
        else:
            try:
                with st.spinner("Ajout du client..."):
                    with get_db_connection() as conn:
                        conn.execute("""
                            INSERT INTO Client (nom_complet, adresse, ville, code_postal, email, tel)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (nom.strip(), adresse.strip(), ville.strip(), code_postal.strip(), email.strip(), tel.strip()))
                        conn.commit()
                        st.success("✅ Client ajouté avec succès")
                        st.rerun()
            except sqlite3.IntegrityError as e:
                st.error(f"❌ Erreur : {e}")

def add_reservation():
    st.subheader("Nouvelle réservation")
    st.markdown("**Tous les champs sont obligatoires.**")
    
    with st.spinner("Chargement des données..."):
        with get_db_connection() as conn:
            clients = conn.execute("SELECT id_client, nom_complet FROM Client ORDER BY nom_complet").fetchall()
            hotels = conn.execute("SELECT id_hotel, ville FROM Hotel").fetchall()
            types_chambre = conn.execute("SELECT id_type, libelle, tarif FROM TypeChambre").fetchall()

    if not hotels:
        st.error("❌ Aucun hôtel disponible. Veuillez ajouter un hôtel d'abord.")
        return

    client_options = {f"{c['nom_complet']} (ID {c['id_client']})": c['id_client'] for c in clients}
    hotel_options = {h["ville"]: h["id_hotel"] for h in hotels}
    type_chambre_options = {f"{t['libelle']} ({t['tarif']}€/nuit)": t['id_type'] for t in types_chambre}

    with st.form("form_reservation"):
        col1, col2 = st.columns(2)
        with col1:
            client_nom = st.selectbox("Client *", ["Sélectionner un client"] + list(client_options.keys()))
            date_arrivee = st.date_input("Date d'arrivée *", min_value=date.today())
            num_rooms = st.number_input("Nombre de chambres *", min_value=1, step=1)
        with col2:
            date_depart = st.date_input("Date de départ *", min_value=date.today())
            hotel = st.selectbox("Hôtel *", ["Sélectionner un hôtel"] + list(hotel_options.keys()))
            type_chambre = st.selectbox("Type de chambre *", ["Sélectionner un type"] + list(type_chambre_options.keys()))

        # Prestations available at selected hotel
        prestations = []
        if hotel != "Sélectionner un hôtel":
            with get_db_connection() as conn:
                prestations = conn.execute("""
                    SELECT p.id_prestation, p.libelle, p.prix 
                    FROM Prestation p
                    JOIN Hotel_Prestation hp ON p.id_prestation = hp.id_prestation
                    WHERE hp.id_hotel = ?
                    """, [hotel_options[hotel]]).fetchall()

        selected_prestations = []
        if prestations:
            st.write("**Prestations disponibles :**")
            selected_prestations = st.multiselect(
                "Sélectionner les prestations (optionnel)",
                options=[f"{p['libelle']} ({p['prix']}€)" for p in prestations],
                default=[]
            )

        submit = st.form_submit_button("Réserver")

    if submit:
        missing_fields = []
        if client_nom == "Sélectionner un client": missing_fields.append("Client")
        if hotel == "Sélectionner un hôtel": missing_fields.append("Hôtel")
        if type_chambre == "Sélectionner un type": missing_fields.append("Type de chambre")
        if not date_arrivee: missing_fields.append("Date d'arrivée")
        if not date_depart: missing_fields.append("Date de départ")

        if missing_fields:
            st.error(f"❌ Veuillez remplir tous les champs obligatoires : {', '.join(missing_fields)}")
        elif date_depart <= date_arrivee:
            st.error("❌ La date de départ doit être après la date d'arrivée.")
        else:
            with st.spinner("Création de la réservation..."):
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    try:
                        # Insert reservation
                        cursor.execute("""
                            INSERT INTO Reservation (date_arrivee, date_depart, id_client)
                            VALUES (?, ?, ?)
                        """, (date_arrivee.isoformat(), date_depart.isoformat(), client_options[client_nom]))
                        reservation_id = cursor.lastrowid

                        # Get available rooms
                        query = """
                        SELECT ch.id_chambre
                        FROM Chambre ch
                        JOIN Hotel h ON ch.id_hotel = h.id_hotel
                        WHERE ch.id_type = ?
                        AND h.id_hotel = ?
                        AND ch.id_chambre NOT IN (
                            SELECT rc.id_chambre
                            FROM Reservation_Chambre rc
                            JOIN Reservation r ON rc.id_reservation = r.id_reservation
                            WHERE NOT (r.date_depart <= ? OR r.date_arrivee >= ?)
                        )
                        LIMIT ?
                        """
                        params = [
                            type_chambre_options[type_chambre], 
                            hotel_options[hotel], 
                            date_arrivee.isoformat(), 
                            date_depart.isoformat(), 
                            num_rooms
                        ]
                        available_rooms = cursor.execute(query, params).fetchall()

                        if len(available_rooms) < num_rooms:
                            st.error(f"❌ Pas assez de chambres disponibles ({len(available_rooms)} disponibles pour {num_rooms} demandées).")
                            conn.rollback()
                        else:
                            # Insert selected rooms
                            for room in available_rooms:
                                cursor.execute("""
                                    INSERT INTO Reservation_Chambre (id_reservation, id_chambre)
                                    VALUES (?, ?)
                                """, (reservation_id, room['id_chambre']))

                            # Insert selected prestations
                            for prest in selected_prestations:
                                prest_name = prest.split(' (')[0]
                                prest_id = next(p['id_prestation'] for p in prestations if p['libelle'] == prest_name)
                                cursor.execute("""
                                    INSERT INTO Reservation_Prestation (id_reservation, id_prestation)
                                    VALUES (?, ?)
                                """, (reservation_id, prest_id))

                            conn.commit()
                            st.success(f"✅ Réservation enregistrée (ID: {reservation_id})")
                            st.rerun()
                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ Erreur lors de la réservation : {str(e)}")

def view_available_rooms():
    st.subheader("Chambres disponibles")
    col1, col2 = st.columns(2)
    with col1:
        date1 = st.date_input("Du", min_value=date.today(), key="date1")
    with col2:
        date2 = st.date_input("Au", min_value=date.today(), key="date2")

    with get_db_connection() as conn:
        hotels = conn.execute("SELECT id_hotel, ville FROM Hotel").fetchall()
    hotel = st.selectbox("Filtrer par hôtel", ["Tous"] + [h["ville"] for h in hotels])

    if st.button("Rechercher"):
        if date2 <= date1:
            st.error("❌ La date 'Au' doit être après la date 'Du'.")
        else:
            with st.spinner("Recherche des chambres disponibles..."):
                with get_db_connection() as conn:
                    query = """
                    SELECT ch.id_chambre, h.ville AS hotel, t.libelle AS type, t.tarif,
                           CASE WHEN ch.fumeurs = 1 THEN 'Oui' ELSE 'Non' END AS fumeurs,
                           ch.etage
                    FROM Chambre ch
                    JOIN Hotel h ON ch.id_hotel = h.id_hotel
                    JOIN TypeChambre t ON ch.id_type = t.id_type
                    WHERE ch.id_chambre NOT IN (
                        SELECT rc.id_chambre
                        FROM Reservation_Chambre rc
                        JOIN Reservation r ON rc.id_reservation = r.id_reservation
                        WHERE NOT (r.date_depart <= ? OR r.date_arrivee >= ?)
                    )
                    """
                    params = [date1.isoformat(), date2.isoformat()]
                    if hotel != "Tous":
                        query += " AND h.id_hotel = ?"
                        params.append(next(h['id_hotel'] for h in hotels if h['ville'] == hotel))

                    df = pd.read_sql_query(query, conn, params=params)
                    if df.empty:
                        st.warning("⚠️ Aucune chambre disponible pour ces dates.")
                    else:
                        st.dataframe(df, use_container_width=True, hide_index=True)

def main():
    render_navigation()
    page_functions = {
        "Voir les réservations": view_reservations,
        "Voir les clients": view_clients,
        "Ajouter un client": add_client,
        "Ajouter une réservation": add_reservation,
        "Voir les chambres disponibles": view_available_rooms
    }
    page_functions[st.session_state.page]()

if __name__ == "__main__":
    main()