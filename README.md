Hotel Management Project - Projet BD 2025

Overview

This repository contains part of the deliverables for the "Projet Bases de Données 2025" for the Licence IAP S4 course, supervised by Pr. J. Zahir. The project was collaboratively developed by Walid Amjahdi and Imane Ait Mbarek. It involves creating and querying a hotel management database using MySQL and SQLite, along with a web interface built using Streamlit.

The project is divided into two parts:





Partie 1: Creating a MySQL database, populating it with provided data, and writing SQL and relational algebra queries.



Partie 2: Building a SQLite database and a Streamlit web interface to manage reservations, clients, and available rooms.

Repository Contents





app.py: Streamlit application for the web interface.



create_db.py: Python script to create and populate the SQLite database.



db.sqlite: SQLite database file (pre-generated for convenience).



init_db.sql: SQL script for initializing the database structure (table creation).



insert_data.sql: SQL script for inserting the provided data into the tables.



README.md: This file.

Note: The video demonstration (Nexus Hotel - Gestion.mp4), relational algebra queries, and combined SQL script (Hotel_Database.sql) are submitted separately in Google Classroom.




The interface allows you to:





View the list of reservations.



View the list of clients.



Check available rooms for a given date range.



Add a new client.



Add a new reservation.

Project Structure

Hotel-Management-Project/
├── app.py              # Streamlit application for the web interface
├── create_db.py        # Script to create and populate the SQLite database
├── db.sqlite           # SQLite database file (pre-generated)
├── init_db.sql         # SQL for database initialization
├── insert_data.sql     # SQL for data insertion
├── README.md           # This file

Demonstration

A video demonstrating the Streamlit interface is available at: https://drive.google.com/file/d/1LY5xh5pSlPJ90J2QAkQGxZJm3d2uHH-g/view?usp=sharing

Submission Notes





Relational Algebra Queries: Submitted as Relational_Algebra_Queries.pdf in Google Classroom.



SQL Script: The init_db.sql and insert_data.sql files are included here, but the complete Hotel_Database.sql (including table creation, data insertion, and queries) is submitted in Google Classroom.



Video Demo: The video (Nexus Hotel - Gestion.mp4) is uploaded to Google Drive or YouTube, and the link is provided in the Google Classroom submission.



GitHub: This repository contains the Streamlit app and SQLite database files. The repository URL is provided in the Google Classroom submission.
