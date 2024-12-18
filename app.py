import streamlit as st
import csv
import os
import pandas as pd

# Dummy data for login and teams
USERS = {
    "user1": {"password": "password1", "teams": ["Tim A", "Tim B"], "is_admin": False},
    "user2": {"password": "password2", "teams": ["Tim C", "Tim A", "Tim D"], "is_admin": False},
    "admin": {"password": "adminpass", "teams": [], "is_admin": True},  # Admin user
}

TEAMS = {
    "Tim A": {"Ketua Tim": ["Kandidat 1", "Kandidat 2", "Kandidat 3"], "Coach": ["Coach 1", "Coach 2"]},
    "Tim B": {"Ketua Tim": ["Kandidat A", "Kandidat B"], "Coach": ["Coach X", "Coach Y", "Coach Z"]},
    "Tim C": {"Ketua Tim": ["Ketua 1", "Ketua 2"], "Coach": ["Coach Alpha", "Coach Beta"]},
    "Tim D": {"Ketua Tim": ["Ketua D1", "Ketua D2"], "Coach": ["Coach Delta1", "Coach Delta2"]},
    "Tim E": {"Ketua Tim": ["Ketua E1", "Ketua E2"], "Coach": ["Coach E1", "Coach E2", "Coach E3"]},
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
            st.session_state.is_admin = USERS[username]["is_admin"]
            st.session_state.current_team_index = 0
            st.session_state.selections = []
            st.session_state.has_submitted = False
        else:
            st.error("Username atau password salah.")

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(selection):
    filename = "selections.csv"

    # Jika file tidak ada, buat header terlebih dahulu
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only if file is new
        if not file_exists:
            writer.writerow(["username", "team", "ketua", "coach"])

        # Menyimpan data pemilihan ke CSV
        writer.writerow(selection)

# Fungsi untuk menampilkan ringkasan isian pengguna
def user_summary():
    st.subheader("Ringkasan Isian Anda")
    filename = "selections.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        user_data = df[df["username"] == st.session_state.username]
        if not user_data.empty:
            st.dataframe(user_data)
        else:
            st.warning("Belum ada data yang Anda isi.")

# Form pemilihan untuk tim tertentu
def selection_form():
    if st.session_state.has_submitted:
        st.warning("Anda sudah mengisi formulir. Berikut adalah ringkasan isian Anda.")
        user_summary()
        return

    team_index = st.session_state.current_team_index
    if team_index < len(st.session_state.teams):
        team = st.session_state.teams[team_index]
        st.subheader(f"Pemilihan untuk {team}")

        ketua = st.radio(f"Pilih Ketua Tim untuk {team}:", TEAMS[team]["Ketua Tim"], key=f"{team}_ketua")
        coach = st.radio(f"Pilih Coach untuk {team}:", TEAMS[team]["Coach"], key=f"{team}_coach")

        if st.button("Next"):
            st.session_state.selections.append([st.session_state.username, team, ketua, coach])
            st.session_state.current_team_index += 1

    else:
        if st.button("Finish"):
            for selection in st.session_state.selections:
                save_to_csv(selection)
            st.session_state.has_submitted = True
            st.success("Data berhasil disimpan.")
            user_summary()

# Fungsi untuk menampilkan data admin
def admin_view():
    filename = "selections.csv"
    st.title("Admin View")
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        st.dataframe(df)

        # Tombol untuk mengunduh file CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV", data=csv_data, file_name="selections.csv", mime="text/csv")
    else:
        st.warning("Belum ada data pemilihan yang tersimpan.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.finished = False
        st.session_state.current_team_index = 0
        st.session_state.selections = []
        st.session_state.has_submitted = False

# Main aplikasi
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "finished" not in st.session_state:
    st.session_state.finished = False
if "has_submitted" not in st.session_state:
    st.session_state.has_submitted = False

if st.session_state.logged_in:
    if st.session_state.is_admin:
        admin_view()
    else:
        selection_form()
else:
    login()
