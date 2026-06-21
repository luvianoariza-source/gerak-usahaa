import streamlit as st
import pandas as pd
import requests

# 1. PENGATURAN LOGO DAN BANNER
LOGO_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/logoGU.png"
BANNER_URL = "https://raw.githubusercontent.com/luvianoariza-source/gerak-usahaa/main/bannerGU.png"

# Menampilkan Logo sebagai ikon browser
st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# Menampilkan Banner Utama
st.image(BANNER_URL, use_column_width=True)

# (Lanjutkan dengan kode form dan lainnya seperti biasa...)
# Tempel Link URL Aplikasi Web (dari Apps Script) di sini:
URL_SIMPAN_DATA = "https://script.google.com/macros/s/AKfycbzX7JBZSHW-ddSs2ago_fYYX8l4R4jGYsS3x2VqbLfT4HZI5uevq522KQj656UatlkAUQ/exec"

# Tempel Link Google Sheets (yang hak aksesnya Editor) di sini:
URL_BACA_DATA = "https://docs.google.com/spreadsheets/d/1eBL-357PBj2LgpZfD-lBk-pcVSYHC_u8dZpethZqZwA/edit?usp=sharing"


# (Mesin otomatis menyesuaikan link Google Sheets Anda - JANGAN DIUBAH)
if "edit" in URL_BACA_DATA:
    URL_BACA_DATA = URL_BACA_DATA.replace("/edit?usp=sharing", "/export?format=csv")
    URL_BACA_DATA = URL_BACA_DATA.replace("/edit", "/export?format=csv")


# === 2. PENGATURAN KONFIGURASI HALAMAN DAN TAMPILAN UI ===

# Mengubah logo aplikasi (ikon browser) dengan file logo.png Anda
st.set_page_config(page_title="Gerak Usaha", page_icon=LOGO_URL, layout="wide")

# Memasang Banner Sampul Aplikasinya (Gambar image_2.png) di paling atas
st.image(BANNER_URL, use_column_width=True)

# st.title("🏢 Gerak Usaha") # Menghapus title bawaan karena sudah ada di banner

# UI Form Input Data (Sisa kode tidak berubah)
st.markdown("---")
with st.expander("➕ Tambah Transaksi Baru", expanded=True):
    with st.form("form_transaksi", clear_on_submit=True):
        kol1, kol2, kol3, kol4 = st.columns(4) # Membuat UI terbagi 4 kolom sejajar
        
        with kol1:
            tgl = st.date_input("Tanggal")
        with kol2:
            omzet = st.number_input("Omzet (Rp)", min_value=0)
        with kol3:
            pengeluaran = st.number_input("Pengeluaran (Rp)", min_value=0)
        with kol4:
            pelanggan = st.number_input("Jumlah Pelanggan", min_value=0)
            
        tombol = st.form_submit_button("Simpan Data")
        
        if tombol:
            laba = omzet - pengeluaran
            # Membungkus data untuk dikirim
            data_kirim = {
                "tanggal": str(tgl),
                "omzet": omzet,
                "pengeluaran": pengeluaran,
                "laba": laba,
                "pelanggan": pelanggan
            }
            
            # Mengirim data ke Google Sheets
            try:
                requests.post(URL_SIMPAN_DATA, json=data_kirim)
                st.success("Data berhasil dikirim ke Google Sheets!")
            except:
                st.error("Gagal mengirim data. Periksa kembali link Apps Script Anda.")

# === 3. UI TAMPILAN DATA & GRAFIK ===
st.subheader("📋 Ringkasan Data")

# Mengambil data dari Google Sheets untuk ditampilkan
try:
    df = pd.read_csv(URL_BACA_DATA)
    if not df.empty:
        # Menampilkan Angka Metrik
        k1, k2, k3 = st.columns(3)
        k1.metric("Total Omzet", f"Rp {df['Omzet'].sum():,.0f}")
        k2.metric("Total Laba", f"Rp {df['Laba Bersih'].sum():,.0f}")
        k3.metric("Total Pelanggan", f"{df['Pelanggan'].sum()} Orang")
        
        st.markdown("---")
        
        # Menampilkan Grafik Garis Laba Bersih
        st.write("📈 Grafik Laba Bersih Harian")
        st.line_chart(df.set_index('Tanggal')['Laba Bersih'])
        
        # Menampilkan Tabel Mentah
        st.write("Riwayat Transaksi")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data di Google Sheets. Silakan isi form di atas.")
except:
    st.warning("Menunggu data dari Google Sheets atau periksa kembali Link Anda.")
