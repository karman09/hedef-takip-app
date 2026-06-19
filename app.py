import streamlit as st
import pandas as pd
import datetime
import os

# Sayfa Genişliği ve Ayarları
st.set_page_config(page_title="Başarı Takip", layout="wide")

# --- Kullanıcı ve Resim Eşleşmeleri ---
kullanici_sozlugu = {
    "Gizem": "Gizem.png",
    "Gülin": "Gülin.png",
    "Kevser": "Kevser.png",
    "Melek": "melek.png",
    "Tayfun": "tayfun.png"
}

# --- CSS ile Özel Tema ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #1f77b4; text-align: center; }
    div.stButton > button { background-color: #4CAF50; color: white; border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetimi")
st.markdown("---")

# Session state başlatma
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = pd.DataFrame(columns=[
        "Tarih", "Saat", "Ad Soyad", "Konu", "Hedef (Saat)", "Gerçekleşen (Saat)", "Başarı (%)"
    ])

# --- Sidebar: Yeni Kayıt ---
with st.sidebar:
    st.header("📝 Yeni Kayıt")
    
    # Resim için ayrılmış dinamik alan
    resim_alani = st.empty()
    
    with st.form("yeni_kayit", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        saat = st.time_input("Saat", datetime.time(9, 0))

        # --- Kişi Seçimi ---
        isim = st.selectbox("Ad Soyad", list(kullanici_sozlugu.keys()))
        
        konu = st.text_input("Konu Başlığı")
        hedef_saat = st.number_input("Hedeflenen Saat", min_value=0.0, step=0.5)
        gercek_saat = st.number_input("Gerçekleşen Saat", min_value=0.0, step=0.5)
        
        ekle = st.form_submit_button("HEDEFE EKLE 🎯")

    # --- Resmin her seçimde güncellenmesi (Form dışı ama sidebar içi) ---
    if isim in kullanici_sozlugu:
        dosya = kullanici_sozlugu[isim]
        if os.path.exists(dosya):
            resim_alani.image(dosya, width=100)
        else:
            resim_alani.warning(f"Resim bulunamadı: {dosya}")
        
    # --- Kayıt İşlemi ---
    if ekle:
        if konu.strip() == "":
            st.error("Lütfen konu başlığını doldurunuz.")
        else:
            yeni_satir = pd.DataFrame([{
                "Tarih": tarih,
                "Saat": saat,
                "Ad Soyad": isim,
                "Konu": konu,
                "Hedef (Saat)": hedef_saat,
                "Gerçekleşen (Saat)": gercek_saat,
                "Başarı (%)": round((gercek_saat / hedef_saat * 100) if hedef_saat > 0 else 0, 2)
            }])
            st.session_state.veri_listesi = pd.concat([st.session_state.veri_listesi, yeni_satir], ignore_index=True)
            st.success(f"Harika bir adım attın, {isim}! 🌟")

# --- Dashboard ---
st.subheader("📊 İlerleme Paneli")
st.session_state.veri_listesi = st.data_editor(st.session_state.veri_listesi, use_container_width=True)

# --- İstatistikler ve Görselleştirme ---
if not st.session_state.veri_listesi.empty:
    st.divider()
    st.markdown("### Kişisel İlerleme Çubukları")
    
    for _, row in st.session_state.veri_listesi.iterrows():
        cols = st.columns([1, 6])
        isim_row = row['Ad Soyad']
        
        with cols[0]:
            if isim_row in kullanici_sozlugu:
                dosya = kullanici_sozlugu[isim_row]
                if os.path.exists(dosya):
                    st.image(dosya, width=50)
        
        with cols[1]:
            st.write(f"**{isim_row}** - {row['Konu']}")
            st.progress(min(row["Başarı (%)"] / 100, 1.0))
    
    # İndirme Butonu
    csv = st.session_state.veri_listesi.to_csv(index=False).encode('utf-8')
    st.download_button("Tüm Verileri İndir (CSV) 📥", csv, "hedef_takip.csv", "text/csv")
