import firebase_admin
from firebase_admin import credentials, firestore
import json

# Inisialisasi Firebase menggunakan Streamlit Secrets
cred_dict = json.loads(st.secrets["firebase_credentials"])
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
db = firestore.client()

# Dummy data untuk login dan tim terkait
USERS = {
    "user1": {"password": "password1", "teams": ["Tim A", "Tim B"]},
    "user2": {"password": "password2", "teams": ["Tim C", "Tim A", "Tim D"]},
    "user3": {"password": "password3", "teams": ["Tim B", "Tim E"]}
}

TEAMS = {
    "Tim A": {"Ketua Tim": ["Kandidat 1", "Kandidat 2", "Kandidat 3"], "Pelatih": ["Pelatih 1", "Pelatih 2"]},
    "Tim B": {"Ketua Tim": ["Kandidat A", "Kandidat B"], "Pelatih": ["Pelatih X", "Pelatih Y", "Pelatih Z"]},
    "Tim C": {"Ketua Tim": ["Ketua 1", "Ketua 2"], "Pelatih": ["Pelatih Alpha", "Pelatih Beta"]},
    "Tim D": {"Ketua Tim": ["Ketua D1", "Ketua D2"], "Pelatih": ["Pelatih Delta1", "Pelatih Delta2"]},
    "Tim E": {"Ketua Tim": ["Ketua E1", "Ketua E2"], "Pelatih": ["Pelatih E1", "Pelatih E2", "Pelatih E3"]}
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

# Fungsi untuk menyimpan data ke Firestore
def save_to_firestore(username, team, ketua, pelatih):
    db.collection("selections").add({
        "username": username,
        "team": team,
        "ketua": ketua,
        "pelatih": pelatih
    })

# Form pemilihan untuk tim tertentu
def selection_form(team):
    st.subheader(f"Pemilihan untuk {team}")

    ketua = st.radio(f"Pilih Ketua Tim untuk {team}:", TEAMS[team]["Ketua Tim"], key=f"{team}_ketua")
    pelatih = st.radio(f"Pilih Pelatih untuk {team}:", TEAMS[team]["Pelatih"], key=f"{team}_pelatih")

    if st.button(f"Submit untuk {team}", key=f"{team}_submit"):
        save_to_firestore(st.session_state.username, team, ketua, pelatih)
        st.success(f"Data untuk tim {team} berhasil disimpan: Ketua **{ketua}**, Pelatih **{pelatih}**.")

# Main aplikasi
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.title("Form Pemilihan Ketua Tim dan Pelatih")
    for team in st.session_state.teams:
        selection_form(team)
else:
    login()
