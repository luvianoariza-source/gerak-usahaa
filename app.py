import streamlit as st
import pandas as pd
import requests

# 1. KONFIGURASI LINK (PASTIKAN ANDA MENGISI LINK INI)
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"
URL_SIMPAN = "https://script.google.com/macros/s/AKfycbzX7JBZSHW-ddSs2ago_fYYX8l4R4jGYsS3x2VqbLfT4HZI5uevq522KQj656UatlkAUQ/exec"
URL_BACA = "https://docs.google.com/spreadsheets/d/1eBL-357PBj2LgpZfD-lBk-pcVSYHC_u8dZpethZqZwA/edit?usp=sharing"

st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# CSS Agar Form Cantik
st.markdown("""
    <style>
    div[data-testid="stExpander"] { border: 2px solid #00a89d !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.image(BANNER_URL, use_column_width=True)

# 2. FORM INPUT
with st.expander("➕ Tambah Transaksi", expanded=True):
    with st.form("input", clear_on_submit=True):
        cols = st.columns(4)
        tgl = cols[0].date_input("Tanggal")
        omzet = cols[1].number_input("Omzet (Rp)", 0)
        keluar = cols[2].number_input("Keluar (Rp)", 0)
        pel = cols[3].number_input("Pelanggan", 0)
        if st.form_submit_button("Simpan Data"):
            data = {"tanggal": str(tgl), "omzet": omzet, "pengeluaran": keluar, "laba": omzet-keluar, "pelanggan": pel}
            requests.post(URL_SIMPAN, json=data)
            st.success("Data tersimpan! Silakan Refresh halaman untuk melihat hasil.")

# 3. TAMPILAN DATA & GRAFIK (INI YANG TADI HILANG)
st.subheader("📋 Ringkasan Data")

try:
    # Membaca data dari Google Sheets
    link_csv = URL_BACA.replace("/edit", "/export?format=csv")
    df = pd.read_csv(link_csv)
    
    # Menampilkan Grafik
    st.write("📈 Grafik Performa")
    st.line_chart(df.set_index('Tanggal')[['Omzet', 'Laba']])
    
    # Menampilkan Tabel
    st.dataframe(df, use_container_width=True)
except:
    st.info("Belum ada data, silakan isi form di atas.")
