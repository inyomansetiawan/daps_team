import streamlit as st
import gspread

# Dummy data untuk login dan tim terkait
USERS = {
    "user1": {"password": "password1", "teams": ["Tim A", "Tim B"]},
    "user2": {"password": "password2", "teams": ["Tim C", "Tim A", "Tim D"]},
    "user3": {"password": "password3", "teams": ["Tim B", "Tim E"]},
}

# Data tim dengan kandidat ketua dan pelatih
TEAMS = {
    "Tim A": {"Ketua Tim": ["Kandidat 1", "Kandidat 2", "Kandidat 3"], "Pelatih": ["Pelatih 1", "Pelatih 2"]},
    "Tim B": {"Ketua Tim": ["Kandidat A", "Kandidat B"], "Pelatih": ["Pelatih X", "Pelatih Y", "Pelatih Z"]},
    "Tim C": {"Ketua Tim": ["Ketua 1", "Ketua 2"], "Pelatih": ["Pelatih Alpha", "Pelatih Beta"]},
    "Tim D": {"Ketua Tim": ["Ketua D1", "Ketua D2"], "Pelatih": ["Pelatih Delta1", "Pelatih Delta2"]},
    "Tim E": {"Ketua Tim": ["Ketua E1", "Ketua E2"], "Pelatih": ["Pelatih E1", "Pelatih E2", "Pelatih E3"]},
}

# Spreadsheet ID (ambil dari URL spreadsheet)
SPREADSHEET_ID = "1mI3kpVWQaCYMQoufi9yuqM13prs14G4IVDMD7gd8BFo"

# Fungsi untuk menghubungkan ke Google Sheets menggunakan akses publik
def connect_to_google_sheets(sheet_id):
    # Menghubungkan ke spreadsheet tanpa autentikasi menggunakan akses publik
    client = gspread.Client(None)  # Tidak menggunakan autentikasi
    return client.open_by_key(sheet_id).sheet1  # Mengakses sheet pertama

# Fungsi untuk menyimpan data ke Google Sheets
def save_to_google_sheets(sheet_id, username, team, ketua, pelatih):
    sheet = connect_to_google_sheets(sheet_id)
    sheet.append_row([username, team, ketua, pelatih])

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

# Form pemilihan untuk tim tertentu
def selection_form(team):
    st.subheader(f"Pemilihan untuk {team}")
    
    ketua = st.radio(f"Pilih Ketua Tim untuk {team}:", TEAMS[team]["Ketua Tim"], key=f"{team}_ketua")
    pelatih = st.radio(f"Pilih Pelatih untuk {team}:", TEAMS[team]["Pelatih"], key=f"{team}_pelatih")
    
    if st.button(f"Submit untuk {team}", key=f"{team}_submit"):
        save_to_google_sheets(SPREADSHEET_ID, st.session_state.username, team, ketua, pelatih)
        st.success(f"Anda telah memilih **{ketua}** sebagai Ketua Tim dan **{pelatih}** sebagai Pelatih untuk {team}.")

# Main aplikasi
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.title("Form Pemilihan Ketua Tim dan Pelatih")
    for team in st.session_state.teams:
        selection_form(team)
else:
    login()
