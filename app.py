import streamlit as st
import csv
import os

# Dummy data for login and teams
USERS = {
    "user1": {"password": "password1", "teams": ["Tim A", "Tim B"]},
    "user2": {"password": "password2", "teams": ["Tim C", "Tim A", "Tim D"]},
    "user3": {"password": "password3", "teams": ["Tim B", "Tim E"]}
}

TEAMS = {
    "Tim A": {"Ketua Tim": ["Kandidat 1", "Kandidat 2", "Kandidat 3"], "Coach": ["Coach 1", "Coach 2"]},
    "Tim B": {"Ketua Tim": ["Kandidat A", "Kandidat B"], "Coach": ["Coach X", "Coach Y", "Coach Z"]},
    "Tim C": {"Ketua Tim": ["Ketua 1", "Ketua 2"], "Coach": ["Coach Alpha", "Coach Beta"]},
    "Tim D": {"Ketua Tim": ["Ketua D1", "Ketua D2"], "Coach": ["Coach Delta1", "Coach Delta2"]},
    "Tim E": {"Ketua Tim": ["Ketua E1", "Ketua E2"], "Coach": ["Coach E1", "Coach E2", "Coach E3"]}
}

# Fungsi untuk login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in USERS and USERS[username]["password"] == password:
            st.success("Login berhasil!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.teams = USERS[username]["teams"]
        else:
            st.error("Username atau password salah.")

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(username, team, ketua, coach):
    # Tentukan nama file CSV
    filename = "selections.csv"
    
    # Jika file tidak ada, buat header terlebih dahulu
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        # Write header only if file is new
        if not file_exists:
            writer.writerow(["username", "team", "ketua", "coach"])
        
        # Menyimpan data pemilihan ke CSV
        writer.writerow([username, team, ketua, coach])

# Form pemilihan untuk tim tertentu
def selection_form(team):
    st.subheader(f"Pemilihan untuk {team}")

    ketua = st.radio(f"Pilih Ketua Tim untuk {team}:", TEAMS[team]["Ketua Tim"], key=f"{team}_ketua")
    coach = st.radio(f"Pilih Coach untuk {team}:", TEAMS[team]["Coach"], key=f"{team}_coach")

    if st.button(f"Submit untuk {team}", key=f"{team}_submit"):
        save_to_csv(st.session_state.username, team, ketua, coach)
        st.success(f"Data untuk tim {team} berhasil disimpan: Ketua **{ketua}**, Coach **{coach}**.")

# Main aplikasi
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.title("Form Pemilihan Ketua Tim dan Coach")
    for team in st.session_state.teams:
        selection_form(team)
else:
    login()
