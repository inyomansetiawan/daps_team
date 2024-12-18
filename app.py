import streamlit as st
import csv
import os
import pandas as pd

# Dummy data for login and teams
USERS = {
    "adi.nugroho": {"password": "Z7j5#e2T", "teams": ["Tim ", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "adwi.hastuti": {"password": "P8k1!vL9", "teams": ["Tim ", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "alvina.clarissa": {"password": "W3t@h4A1", "teams": ["Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "ana.fitriyani": {"password": "J2q8K@b5", "teams": ["Tim DEV_QA & PERBAN", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "aprilia.pratiwi": {"password": "M7l9U#r4", "teams": ["Tim CERDAS", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "bayu.kurniawan": {"password": "B3d@V0p1", "teams": ["Tim ASUS", "Tim CERDAS", "Tim ", "Tim "], "is_admin": False},
    "dede.paramartha": {"password": "H4m5!V7Q", "teams": ["Tim ASUS", "Tim CERDAS", "Tim DS", "Tim "], "is_admin": False},
    "dewi.krismawati": {"password": "D9g$H6o3", "teams": ["Tim CERDAS", "Tim DS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "dewi.amaliah": {"password": "J2r@Y8pL", "teams": ["Tim CERDAS", "Tim DEV_QA & PERBAN", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "dewi.widyawati": {"password": "L0v6R#y8", "teams": ["Tim ASUS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "dhiar.larasati": {"password": "S4v9A@t5", "teams": ["Tim CERDAS", "Tim DS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "dyah.prihatinningsih": {"password": "T5u6@C7d", "teams": ["Tim ASUS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "ema.tusianti": {"password": "F1n9M3eL", "teams": ["Tim ASUS", "Tim CERDAS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "erna.yulianingsih": {"password": "R2d6!K4q", "teams": ["Tim CERDAS", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "ety.kurniati": {"password": "L7s@B9pA", "teams": ["Tim ", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "farhan.arsyi": {"password": "Q8k1T@v7", "teams": ["Tim DS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "nyoman.setiawan": {"password": "Y4b6U!p9", "teams": ["Tim CERDAS", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "julita.aritonang": {"password": "F1t9P@r7", "teams": ["Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "khairunnisah": {"password": "X6n1I9mS", "teams": ["Tim ASUS", "Tim DS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "lika.fuaida": {"password": "D7p9C2eL", "teams": ["Tim ASUS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "maria.widiatma": {"password": "S3r8T4aD", "teams": ["Tim DEV_QA & PERBAN", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "mohammad.alwandi": {"password": "M6a9A1oW", "teams": ["Tim ASUS", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "muhammad.ihsan": {"password": "A3b7V5nI", "teams": ["Tim CERDAS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "muhammad.riyadi": {"password": "P8o4I2yR", "teams": ["Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "nabila.putri": {"password": "O2p7B9qA", "teams": ["Tim CERDAS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "nensi.deli": {"password": "G5w8D0sF", "teams": ["Tim CERDAS", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "nia.setiyawati": {"password": "K3m9A2oE", "teams": ["Tim ASUS", "Tim CERDAS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "nurarifin": {"password": "P9e3R7vT", "teams": ["Tim ASUS", "Tim CERDAS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "putri.larasaty": {"password": "Y7k1Q5vA", "teams": ["Tim CERDAS", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "putri.handayani": {"password": "L2b9T1kP", "teams": ["Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "ranu.yulianto": {"password": "S1g8N0aP", "teams": ["Tim CERDAS", "Tim DS", "Tim ", "Tim "], "is_admin": False},
    "reni.amelia": {"password": "O7j5R9uF", "teams": ["Tim ASUS", "Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "ria.noviana": {"password": "K3p8L0tA", "teams": ["Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "sukmasari.dewanti": {"password": "G7j9D2eV", "teams": ["Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "synthia.kristiani": {"password": "V1o5T2kF", "teams": ["Tim DEV_QA & PERBAN", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "syukriyah.delyana": {"password": "W6m8E3jP", "teams": ["Tim ", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "tika.meilaningsih": {"password": "X4t2H8oY", "teams": ["Tim ASUS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "valent.saputri": {"password": "H3k9G7vR", "teams": ["Tim ASUS", "Tim CERDAS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "yohanes.apriliawan": {"password": "J5q1A9bP", "teams": ["Tim ", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "yoyo.karyono": {"password": "T8u3O1fW", "teams": ["Tim ", "Tim ", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "zulfa.putri": {"password": "P7e4F3yA", "teams": ["Tim CERDAS", "Tim DS", "Tim ", "Tim ", "Tim "], "is_admin": False},
    "admin": {"password": "rnvsnb", "teams": [], "is_admin": True},  # Admin user
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
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.teams = USERS[username]["teams"]
            st.session_state.is_admin = USERS[username]["is_admin"]
            st.session_state.selections = []
            st.session_state.has_submitted = False

            # Periksa apakah pengguna sudah mengisi formulir
            check_user_data(username)
        else:
            st.error("Username atau password salah.")

# Fungsi untuk memeriksa apakah pengguna sudah mengisi formulir
def check_user_data(username):
    filename = "selections.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        user_data = df[df["username"] == username]
        if not user_data.empty:
            st.session_state.has_submitted = True
            st.session_state.selections = user_data.values.tolist()

# Fungsi untuk menyimpan data ke file CSV tanpa duplikasi
def save_to_csv(selection):
    filename = "selections.csv"
    file_exists = os.path.isfile(filename)

    # Membaca data CSV yang ada untuk memeriksa duplikasi
    existing_data = pd.DataFrame()
    if file_exists:
        existing_data = pd.read_csv(filename)
    
    # Konversi ke DataFrame
    new_data = pd.DataFrame([selection], columns=["username", "team", "ketua", "coach"])

    # Periksa apakah data sudah ada
    if not existing_data.empty:
        if not existing_data.merge(new_data, how="inner").empty:
            return  # Data sudah ada, tidak perlu ditambahkan
    
    # Jika data belum ada, tambahkan
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["username", "team", "ketua", "coach"])  # Tulis header jika file baru
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

# Form pemilihan untuk tim tertentu dalam satu halaman
def selection_form():
    if st.session_state.has_submitted:
        st.warning("Anda sudah mengisi formulir. Berikut adalah ringkasan isian Anda.")
        user_summary()
        if st.button("Logout"):
            logout()
        return

    st.subheader("Form Pemilihan Tim")

    # Menampilkan formulir untuk setiap tim
    for team in st.session_state.teams:
        st.write(f"**{team}**")
        ketua = st.radio(f"Pilih Ketua Tim untuk {team}:", TEAMS[team]["Ketua Tim"], key=f"{team}_ketua")
        coach = st.radio(f"Pilih Coach untuk {team}:", TEAMS[team]["Coach"], key=f"{team}_coach")
        
        # Menyimpan pilihan pengguna
        if ketua and coach:
            st.session_state.selections.append([st.session_state.username, team, ketua, coach])

    # Tombol Selesai dan tampilkan hasil
    if st.button("Selesai"):
        for selection in st.session_state.selections:
            save_to_csv(selection)
        st.session_state.has_submitted = True

# Fungsi untuk logout
def logout():
    st.session_state.logged_in = False
    st.session_state.selections = []
    st.session_state.has_submitted = False
    st.session_state.username = ""
    st.session_state.teams = []
    st.session_state.is_admin = False
    st.session_state.current_team_index = 0

# Fungsi untuk menampilkan data admin
def admin_view():
    filename = "selections.csv"
    st.title("Admin View")
    
    if os.path.isfile(filename):
        # Membaca data dari CSV
        df = pd.read_csv(filename)
        
        # Menampilkan data pengguna
        st.subheader("Data Pemilihan Ketua Tim dan Coach")
        st.dataframe(df)
        
        # Tombol untuk mengunduh file CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV", data=csv_data, file_name="selections.csv", mime="text/csv")
        
    else:
        st.warning("Belum ada data pemilihan yang tersimpan.")
    
    # Tombol logout
    if st.button("Logout"):
        logout()

# Main aplikasi
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "has_submitted" not in st.session_state:
    st.session_state.has_submitted = False

if st.session_state.logged_in:
    if st.session_state.is_admin:
        admin_view()
    else:
        selection_form()
else:
    login()
