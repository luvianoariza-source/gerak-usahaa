import streamlit as st
import pandas as pd
import requests

# 1. KONFIGURASI LINK
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"
URL_SIMPAN = "PASTE_LINK_APPS_SCRIPT_ANDA_DI_SINI"
URL_BACA = "PASTE_LINK_GOOGLE_SHEETS_ANDA_DI_SINI"

st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# 2. CSS & TAMPILAN
st.markdown("""<style>div[data-testid="stExpander"] { border: 2px solid #00a89d !important; border-radius: 15px; }</style>""", unsafe_allow_html=True)
st.image(BANNER_URL, use_column_width=True)

# 3. FORM INPUT
with st.expander("➕ Tambah Transaksi", expanded=True):
    with st.form("input", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        tgl = c1.date_input("Tanggal")
        omzet = c2.number_input("Omzet (Rp)", 0)
        keluar = c3.number_input("Pengeluaran (Rp)", 0)
        pel = c4.number_input("Pelanggan", 0)
        if st.form_submit_button("Simpan Data"):
            data = {"tanggal": str(tgl), "omzet": omzet, "pengeluaran": keluar, "laba": omzet-keluar, "pelanggan": pel}
            requests.post(URL_SIMPAN, json=data)
            st.success("Tersimpan! Refresh halaman (F5).")

# 4. GRAFIK & TABEL LENGKAP
st.subheader("📋 Ringkasan Data & Grafik")
try:
    link_csv = URL_BACA.replace("/edit", "/export?format=csv")
    df = pd.read_csv(link_csv)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    
    # Menampilkan Grafik dengan semua kolom yang relevan
    st.write("📈 Grafik Kinerja (Omzet, Pengeluaran, Laba)")
    st.line_chart(df.set_index('Tanggal')[['Omzet', 'Pengeluaran', 'Laba']])
    
    # Tabel Lengkap
    st.write("📊 Tabel Data Lengkap")
    st.dataframe(df.sort_values(by='Tanggal', ascending=False), use_container_width=True)

except:
    st.info("Pastikan judul kolom di Google Sheets adalah: Tanggal, Omzet, Pengeluaran, Laba, Pelanggan.")
