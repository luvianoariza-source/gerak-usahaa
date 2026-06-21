import streamlit as st
import pandas as pd

# Konfigurasi
URL_BACA = "PASTE_LINK_CSV_HASIL_PUBLISH_TO_WEB_DISINI"

st.subheader("📋 Ringkasan Data & Grafik")

try:
    # Membaca data
    df = pd.read_csv(URL_BACA)
    
    # 1. Bersihkan spasi di judul kolom
    df.columns = df.columns.str.strip()
    
    # 2. Paksa konversi kolom menjadi angka (angka yang rusak jadi 0)
    cols = ['Omzet', 'Pengeluaran', 'Laba']
    for col in cols:
        if col in df.columns:
            # Menghapus simbol jika ada, lalu ubah jadi angka
            df[col] = df[col].replace({'[Rp,.]': ''}, regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # 3. Konversi Tanggal
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
    df = df.dropna(subset=['Tanggal'])
    
    # 4. Tampilkan grafik dan tabel
    if not df.empty:
        st.line_chart(df.set_index('Tanggal')[['Omzet', 'Pengeluaran', 'Laba']])
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Data kosong atau format salah.")

except Exception as e:
    st.error(f"Error pada grafik: {e}")
