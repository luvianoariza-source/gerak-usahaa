import streamlit as st
import pandas as pd
import requests

# 1. PENGATURAN URL
# Kita tetap menyimpan LOGO_URL untuk ikon tab browser, tapi tidak akan kita tampilkan di badan halaman
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"

# 2. PENGATURAN HALAMAN
# Logo hanya muncul sebagai ikon di tab browser (pojok atas)
st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")
   st.markdown("""
    <style>
    /* Memberikan bingkai tipis berwarna Tosca pada kotak transaksi */
    div[data-testid="stExpander"] {
        border: 1px solid #00a89d !important;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)     
        # (Catatan: Pastikan Anda sudah mengisi URL_SIMPAN_DATA dan URL_BACA_DATA Anda di sini jika diperlukan)

# 3. MENAMPILKAN BANNER
# Hanya banner yang ditampilkan di badan halaman
st.image(BANNER_URL, use_column_width=True)

# 4. FORM INPUT DATA
st.markdown("---")
with st.expander("➕ Tambah Transaksi Baru", expanded=True):
    with st.form("form_transaksi", clear_on_submit=True):
        kol1, kol2, kol3, kol4 = st.columns(4)
        
        with kol1:
            tgl = st.date_input("Tanggal")
        with kol2:
            omzet = st.number_input("Omzet (Rp)", min_value=0)
        with kol3:
            pengeluaran = st.number_input("Pengeluaran (Rp)", min_value=0)
        with kol4:
            pelanggan = st.number_input("Jumlah Pelanggan", min_value=0)
            
        tombol = st.form_submit_button("Simpan Data")
    


# 5. RINGKASAN DATA
st.subheader("📋 Ringkasan Data")
# ... (lanjutkan sisa kode untuk menampilkan tabel dan grafik Anda)
