import streamlit as st
import pandas as pd
import requests

# --- 1. KONFIGURASI LINK (WAJIB DIISI) ---
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"
URL_SIMPAN = "https://script.google.com/macros/s/AKfycbzX7JBZSHW-ddSs2ago_fYYX8l4R4jGYsS3x2VqbLfT4HZI5uevq522KQj656UatlkAUQ/exec
"
URL_BACA = "https://docs.google.com/spreadsheets/d/1eBL-357PBj2LgpZfD-lBk-pcVSYHC_u8dZpethZqZwA/edit?usp=sharing"

# --- 2. SETUP HALAMAN ---
st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# --- 3. CSS (Tampilan Cantik) ---
st.markdown("""
    <style>
    div[data-testid="stExpander"] { border: 2px solid #00a89d !important; border-radius: 15px; }
    .stApp { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TAMPILAN BANNER ---
st.image(BANNER_URL, use_column_width=True)

# --- 5. FORM INPUT DATA ---
with st.expander("➕ Tambah Transaksi", expanded=True):
    with st.form("input", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        tgl = c1.date_input("Tanggal")
        omzet = c2.number_input("Omzet (Rp)", 0)
        keluar = c3.number_input("Pengeluaran (Rp)", 0)
        pel = c4.number_input("Pelanggan", 0)
        
        if st.form_submit_button("Simpan Data"):
            data = {"tanggal": str(tgl), "omzet": omzet, "pengeluaran": keluar, "laba": omzet-keluar, "pelanggan": pel}
            try:
                requests.post(URL_SIMPAN, json=data)
                st.success("Data tersimpan! Refresh halaman (F5) untuk update grafik.")
            except:
                st.error("Gagal mengirim data.")

# --- 6. GRAFIK & TABEL LENGKAP ---
st.subheader("📋 Ringkasan Data & Grafik")
try:
    link_csv = URL_BACA.replace("/edit", "/export?format=csv")
    df = pd.read_csv(link_csv)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    
    # Grafik dengan Omzet, Pengeluaran, dan Laba
    st.write("📈 Grafik Kinerja (Omzet, Pengeluaran, Laba)")
    st.line_chart(df.set_index('Tanggal')[['Omzet', 'Pengeluaran', 'Laba']])
    
    # Tabel Data
    st.write("📊 Tabel Data Lengkap")
    st.dataframe(df.sort_values(by='Tanggal', ascending=False), use_container_width=True)
except:
    st.info("Menunggu data dari Google Sheets. Pastikan kolom di Sheets: Tanggal, Omzet, Pengeluaran, Laba, Pelanggan.")
