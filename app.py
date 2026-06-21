import streamlit as st
import pandas as pd
import requests

# Link Gambar (Sudah benar)
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"

# Setup Halaman
st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# CSS Agar Form Cantik & Tidak ada Logo Ganda
st.markdown("""
    <style>
    div[data-testid="stExpander"] { border: 2px solid #00a89d !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Tampilkan Banner Saja
st.image(BANNER_URL, use_column_width=True)

# Form Input
with st.expander("➕ Tambah Transaksi", expanded=True):
    with st.form("input", clear_on_submit=True):
        cols = st.columns(4)
        tgl = cols[0].date_input("Tanggal")
        omzet = cols[1].number_input("Omzet (Rp)", 0)
        keluar = cols[2].number_input("Keluar (Rp)", 0)
        pel = cols[3].number_input("Pelanggan", 0)
        if st.form_submit_button("Simpan"):
            st.success("Tersimpan!")

st.subheader("📋 Ringkasan Data")
