import streamlit as st
import pandas as pd
import requests

# 1. KONFIGURASI LINK
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"
URL_SIMPAN = "PASTE_LINK_APPS_SCRIPT_ANDA_DI_SINI"
URL_BACA = "PASTE_LINK_GOOGLE_SHEETS_ANDA_DI_SINI"

st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# 2. CSS
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
            st.success("Tersimpan! Refresh halaman untuk melihat grafik.")

# 4. PEMROSESAN & GRAFIK
st.subheader("📋 Ringkasan Data & Grafik")
try:
    link_csv = URL_BACA.replace("/edit", "/export?format=csv")
    df = pd.read_csv(link_csv)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    
    # Pilihan Tampilan
    tab1, tab2, tab3 = st.tabs(["Harian", "Bulanan", "Tahunan"])
    
    with tab1:
        st.line_chart(df.set_index('Tanggal')[['Omzet', 'Laba']])
        
    with tab2:
        df_bulan = df.resample('ME', on='Tanggal')[['Omzet', 'Laba']].sum()
        st.bar_chart(df_bulan)
        
    with tab3:
        df_tahun = df.resample('YE', on='Tanggal')[['Omzet', 'Laba']].sum()
        st.bar_chart(df_tahun)

    st.dataframe(df, use_container_width=True)
except:
    st.info("Data belum terbaca. Pastikan kolom di Sheets: Tanggal, Omzet, Laba, Pelanggan.")
