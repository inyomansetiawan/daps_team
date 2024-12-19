import streamlit as st
import csv
import os
import pandas as pd

# Dummy data for login and teams
USERS = {
    "adi.nugroho": {"password": "Z7j5#e2T", "teams": ["Tim IPMPLUS", "Tim SAE", "Tim SD", "Tim SDGs", "Tim KMD"], "is_admin": False},
    "adwi.hastuti": {"password": "P8k1!vL9", "teams": ["Tim PSS", "Tim PVD", "Tim REPO", "Tim SAKIP", "Tim SDGs"], "is_admin": False},
    "alvina.clarissa": {"password": "W3t@h4A1", "teams": ["Tim FMS", "Tim IPMPLUS", "Tim KMD", "Tim SD"], "is_admin": False},
    "ana.fitriyani": {"password": "J2q8K@b5", "teams": ["Tim DEV_QA & PERBAN", "Tim DS", "Tim REPO", "Tim SAKIP"], "is_admin": False},
    "aprilia.pratiwi": {"password": "M7l9U#r4", "teams": ["Tim CERDAS", "Tim REPO", "Tim SAKIP", "Tim SAE", "Tim SDGs"], "is_admin": False},
    "bayu.kurniawan": {"password": "B3d@V0p1", "teams": ["Tim ASUS", "Tim CERDAS", "Tim SAE", "Tim SD"], "is_admin": False},
    "dede.paramartha": {"password": "H4m5!V7Q", "teams": ["Tim ASUS", "Tim CERDAS", "Tim DS", "Tim QG"], "is_admin": False},
    "dewi.krismawati": {"password": "D9g$H6o3", "teams": ["Tim CERDAS", "Tim DS", "Tim GENAI", "Tim PSS", "Tim SAE"], "is_admin": False},
    "dewi.amaliah": {"password": "J2r@Y8pL", "teams": ["Tim CERDAS", "Tim DEV_QA & PERBAN", "Tim DS", "Tim GENAI", "Tim PSS"], "is_admin": False},
    "dewi.widyawati": {"password": "L0v6R#y8", "teams": ["Tim ASUS", "Tim PVD", "Tim SAE", "Tim SD"], "is_admin": False},
    "dhiar.larasati": {"password": "S4v9A@t5", "teams": ["Tim CERDAS", "Tim DS", "Tim GENAI", "Tim PSS", "Tim SAE"], "is_admin": False},
    "dyah.prihatinningsih": {"password": "T5u6@C7d", "teams": ["Tim ASUS", "Tim IPMPLUS", "Tim KMD", "Tim SAKIP"], "is_admin": False},
    "ema.tusianti": {"password": "F1n9M3eL", "teams": ["Tim ASUS", "Tim CERDAS", "Tim KMD", "Tim PVD"], "is_admin": False},
    "erna.yulianingsih": {"password": "R2d6!K4q", "teams": ["Tim CERDAS", "Tim FMS", "Tim PVD", "Tim SD", "Tim SDGs"], "is_admin": False},
    "ety.kurniati": {"password": "L7s@B9pA", "teams": ["Tim IPMPLUS", "Tim PSS", "Tim QG", "Tim SAKIP", "Tim SIQAF"], "is_admin": False},
    "farhan.arsyi": {"password": "Q8k1T@v7", "teams": ["Tim DS", "Tim IPMPLUS", "Tim QG", "Tim SDGs"], "is_admin": False},
    "nyoman.setiawan": {"password": "Y4b6U!p9", "teams": ["Tim CERDAS", "Tim DS", "Tim GENAI", "Tim PVD"], "is_admin": False},
    "julita.aritonang": {"password": "F1t9P@r7", "teams": ["Tim DEV_QA & PERBAN", "Tim QG", "Tim REPO", "Tim SAKIP", "Tim SIQAF"], "is_admin": False},
    "khairunnisah": {"password": "X6n1I9mS", "teams": ["Tim ASUS", "Tim DS", "Tim PSS", "Tim SDGs", "Tim SIQAF"], "is_admin": False},
    "lika.fuaida": {"password": "D7p9C2eL", "teams": ["Tim ASUS", "Tim GENAI", "Tim REPO", "Tim SD"], "is_admin": False},
    "maria.widiatma": {"password": "S3r8T4aD", "teams": ["Tim DEV_QA & PERBAN", "Tim DS", "Tim GENAI", "Tim REPO"], "is_admin": False},
    "mohammad.alwandi": {"password": "M6a9A1oW", "teams": ["Tim ASUS", "Tim DS", "Tim FMS", "Tim REPO"], "is_admin": False},
    "muhammad.ihsan": {"password": "A3b7V5nI", "teams": ["Tim CERDAS", "Tim IPMPLUS", "Tim PVD", "Tim SDGs"], "is_admin": False},
    "muhammad.riyadi": {"password": "P8o4I2yR", "teams": ["Tim DEV_QA & PERBAN", "Tim FMS", "Tim GENAI", "Tim QG"], "is_admin": False},
    "nabila.putri": {"password": "O2p7B9qA", "teams": ["Tim CERDAS", "Tim IPMPLUS", "Tim QG", "Tim REPO"], "is_admin": False},
    "nensi.deli": {"password": "G5w8D0sF", "teams": ["Tim CERDAS", "Tim DS", "Tim GENAI", "Tim REPO"], "is_admin": False},
    "nia.setiyawati": {"password": "K3m9A2oE", "teams": ["Tim ASUS", "Tim CERDAS", "Tim IPMPLUS", "Tim QG", "Tim SD"], "is_admin": False},
    "nurarifin": {"password": "P9e3R7vT", "teams": ["Tim ASUS", "Tim CERDAS", "Tim FMS", "Tim SAE", "Tim SD"], "is_admin": False},
    "putri.larasaty": {"password": "Y7k1Q5vA", "teams": ["Tim CERDAS", "Tim KMD", "Tim PSS", "Tim REPO", "Tim SD"], "is_admin": False},
    "putri.handayani": {"password": "L2b9T1kP", "teams": ["Tim DEV_QA & PERBAN", "Tim KMD", "Tim PSS", "Tim QG", "Tim SAKIP"], "is_admin": False},
    "ranu.yulianto": {"password": "S1g8N0aP", "teams": ["Tim CERDAS", "Tim DS", "Tim GENAI", "Tim SIQAF"], "is_admin": False},
    "reni.amelia": {"password": "O7j5R9uF", "teams": ["Tim ASUS", "Tim DEV_QA & PERBAN", "Tim QG", "Tim SAE", "Tim SIQAF"], "is_admin": False},
    "ria.noviana": {"password": "K3p8L0tA", "teams": ["Tim DEV_QA & PERBAN", "Tim FMS", "Tim PVD", "Tim QG"], "is_admin": False},
    "sukmasari.dewanti": {"password": "G7j9D2eV", "teams": ["Tim DEV_QA & PERBAN", "Tim KMD", "Tim PSS", "Tim PVD", "Tim SDGs"], "is_admin": False},
    "synthia.kristiani": {"password": "V1o5T2kF", "teams": ["Tim DEV_QA & PERBAN", "Tim FMS", "Tim KMD", "Tim PVD", "Tim SIQAF"], "is_admin": False},
    "syukriyah.delyana": {"password": "W6m8E3jP", "teams": ["Tim IPMPLUS", "Tim KMD", "Tim PVD", "Tim QG", "Tim SAKIP"], "is_admin": False},
    "tika.meilaningsih": {"password": "X4t2H8oY", "teams": ["Tim ASUS", "Tim PSS", "Tim SAE", "Tim SDGs"], "is_admin": False},
    "valent.saputri": {"password": "H3k9G7vR", "teams": ["Tim ASUS", "Tim CERDAS", "Tim IPMPLUS", "Tim KMD", "Tim PVD"], "is_admin": False},
    "yohanes.apriliawan": {"password": "J5q1A9bP", "teams": ["Tim GENAI", "Tim QG", "Tim SAE", "Tim SIQAF"], "is_admin": False},
    "yoyo.karyono": {"password": "T8u3O1fW", "teams": ["Tim IPMPLUS", "Tim KMD", "Tim PSS", "Tim SAKIP", "Tim SIQAF"], "is_admin": False},
    "zulfa.putri": {"password": "P7e4F3yA", "teams": ["Tim CERDAS", "Tim DS", "Tim PSS", "Tim REPO", "Tim SAE"], "is_admin": False},
    "admin": {"password": "rnvsnb", "teams": [], "is_admin": True},  # Admin user
}

TEAMS = {
    "Tim ASUS": {"Ketua Tim": ["Reni Amelia", "Khairunnisah", "Nurarifin"], "Coach": ["Arham Rivai", "Taulina Anggarani", "Wisnu Winardi"]},
    "Tim CERDAS": {"Ketua Tim": ["Valent Gigih Saputri", "Dewi Lestari Amaliah", "Bayu Dwi Kurniawan"], "Coach": ["Ambar Dwi Santoso", "Edi Waryono", "Taulina Anggarani"]},
    "Tim DEV_QA & PERBAN": {"Ketua Tim": ["Sukmasari Dewanti", "Putri Wahyu Handayani", "Dewi Lestari Amaliah"], "Coach": ["Usman Bustaman", "Widyayanto Adinugroho", "Yeshri Rahayu"]},
    "Tim DS": {"Ketua Tim": ["Dewi Krismawati", "Ranu Yulianto", "Dede Yoga Paramartha"], "Coach": ["Ambar Dwi Santoso", "Usman Bustaman", "Widyayanto Adinugroho"]},
    "Tim FMS": {"Ketua Tim": ["Nurarifin", "Erna Yulianingsih", "Synthia Natalia Kristiani"], "Coach": ["Ambar Dwi Santoso", "Arham Rivai", "Lestyowati Endang Widyantari"]},
    "Tim GENAI": {"Ketua Tim": ["Dhiar Niken Larasati", "Dewi Lestari Amaliah", "I Nyoman Setiawan"], "Coach": ["Ambar Dwi Santoso", "Mutijo", "Usman Bustaman"]},
    "Tim IPMPLUS": {"Ketua Tim": ["Yoyo Karyono", "Adi Nugroho", "Nia Setiyawati"], "Coach": ["Edi Waryono", "Mutijo", "Wisnu Winardi"]},
    "Tim KMD": {"Ketua Tim": ["Adi Nugroho", "Valent Gigih Saputri", "Putri Larasaty"], "Coach": ["Edi Waryono", "Indah Budiati", "Wisnu Winardi"]},
    "Tim PSS": {"Ketua Tim": ["Putri Wahyu Handayani", "Zulfa Hidayah Satria Putri", "Tika Meilaningsih"], "Coach": ["Arham Rivai", "Taulina Anggarani", "Yeshri Rahayu"]},
    "Tim PVD": {"Ketua Tim": ["Syukriyah Delyana", "Muhammad Ihsan", "Ria Noviana"], "Coach": ["Arham Rivai", "Mutijo", "Wisnu Winardi"]},
    "Tim QG": {"Ketua Tim": ["Reni Amelia", "Yohanes Eki Apriliawan", "Ria Noviana"], "Coach": ["Arham Rivai", "Lestyowati Endang Widyantari", "Widyayanto Adinugroho"]},
    "Tim REPO": {"Ketua Tim": ["Aprilia Ira Pratiwi", "Putri Larasaty", "Mohammad Ammar Alwandi"], "Coach": ["Ambar Dwi Santoso", "Widyayanto Adinugroho", "Yeshri Rahayu"]},
    "Tim SAKIP": {"Ketua Tim": ["Adwi Hastuti", "Ety Kurniati", "Syukriyah Delyana"], "Coach": ["Indah Budiati", "Lestyowati Endang Widyantari", "Taulina Anggarani"]},
    "Tim SAE": {"Ketua Tim": ["Dhiar Niken Larasati", "Dewi Krismawati", "Zulfa Hidayah Satria Putri"], "Coach": ["Edi Waryono", "Mutijo", "Usman Bustaman"]},
    "Tim SD": {"Ketua Tim": ["Adi Nugroho", "Nurarifin", "Dewi Widyawati"], "Coach": ["Indah Budiati", "Mutijo", "Wisnu Winardi"]},
    "Tim SDGs": {"Ketua Tim": ["Khairunnisah", "Erna Yulianingsih", "Aprilia Ira Pratiwi"], "Coach": ["Edi Waryono", "Indah Budiati", "Taulina Anggarani"]},
    "Tim SIQAF": {"Ketua Tim": ["Yohanes Eki Apriliawan", "Synthia Natalia Kristiani", "Ranu Yulianto"], "Coach": ["Lestyowati Endang Widyantari", "Widyayanto Adinugroho", "Yeshri Rahayu"]},
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
        
        # Pilihan ketua dan coach untuk tim tertentu
        ketua = st.radio(f"Pilih Ketua Tim untuk {team}:", TEAMS[team]["Ketua Tim"], key=f"{team}_ketua")
        coach = st.radio(f"Pilih Coach untuk {team}:", TEAMS[team]["Coach"], key=f"{team}_coach")
        
        # Perbarui pilihan jika ada perubahan
        if ketua and coach:
            # Cari dan perbarui data yang ada untuk tim ini
            updated = False
            for i, selection in enumerate(st.session_state.selections):
                if selection[1] == team:
                    st.session_state.selections[i] = [st.session_state.username, team, ketua, coach]
                    updated = True
                    break
            
            # Jika tim belum dipilih, tambahkan pilihan baru
            if not updated:
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
