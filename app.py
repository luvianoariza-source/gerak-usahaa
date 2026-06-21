import streamlit as st
import pandas as pd
import requests

# --- KONFIGURASI ---
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"

# Tempel link Apps Script & Google Sheets Anda di bawah:
URL_SIMPAN_DATA = "https://script.google.com/macros/s/AKfycbzX7JBZSHW-ddSs2ago_fYYX8l4R4jGYsS3x2VqbLfT4HZI5uevq522KQj656UatlkAUQ/exec"
URL_BACA_DATA = "https://docs.google.com/spreadsheets/d/1eBL-357PBj2LgpZfD-lBk-pcVSYHC_u8dZpethZqZwA/edit?usp=sharing"

st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# --- CSS UNTUK TAMPILAN ---
st.markdown("""
    <style>
    div[data-testid="stExpander"] { border: 2px solid #00a89d !important; border-radius: 15px; }
    .stApp { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- TAMPILAN ---
st.image(BANNER_URL, use_column_width=True)

st.markdown("### ➕ Tambah Transaksi Baru")
with st.expander("Klik untuk isi data transaksi", expanded=True):
    with st.form("form_transaksi", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        tgl = c1.date_input("Tanggal")
        omzet = c2.number_input("Omzet (Rp)", min_value=0)
        pengeluaran = c3.number_input("Pengeluaran (Rp)", min_value=0)
        pelanggan = c4.number_input("Jumlah Pelanggan", min_value=0)
        
        if st.form_submit_button("Simpan Data"):
            data = {"tanggal": str(tgl), "omzet": omzet, "pengeluaran": pengeluaran, "laba": omzet-pengeluaran, "pelanggan": pelanggan}
            try:
                requests.post(URL_SIMPAN_DATA, json=data)
                st.success("Data berhasil disimpan!")
            except:
                st.error("Gagal menyimpan data.")

st.markdown("---")
st.subheader("📋 Ringkasan Data")

# Mengambil Data
try:
    if "edit" in URL_BACA_DATA: URL_BACA_DATA = URL_BACA_DATA.replace("/edit", "/export?format=csv")
    df = pd.read_csv(URL_BACA_DATA)
    st.dataframe(df, use_container_width=True)
except:
    st.info("Menunggu data...")
