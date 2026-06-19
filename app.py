import streamlit as st
import pandas as pd
import datetime
import os
import random

# Sayfa Genişliği ve Ayarları
st.set_page_config(page_title="Başarı Takip", layout="wide")

# --- Motivasyon Sözleri Listesi ---
motivasyon_sozleri = [
    "Başarının yolu, denemekten geçer.", "Küçük adımlar, büyük hedeflere götürür.",
    "Bugün, dünden daha fazlasını yapabilirsin.", "Başarı, hazırlık ve fırsatın buluşmasıdır.",
    "Kendine inan, her şeyin yarısını başarmışsın demektir.", "Asla pes etme, büyük şeyler zaman alır.",
    # ... buraya 100 taneye kadar söz ekleyebilirsiniz ...
    "Zorluklar, başarının değerini artıran süslerdir.", "Dün yaptıklarınla yetiniyorsan, henüz hiçbir şey yapmamışsın demektir."
]

# --- Kullanıcı ve Resim Eşleşmeleri ---
kullanici_sozlugu = {
    "Gizem": "Gizem.png",
    "Gülin": "Gülin.png",
    "Kevser": "Kevser.png",
    "Melek": "melek.png",
    "Tayfun": "tayfun.png"
}

# --- CSS ve Başlık ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .soz-kutusu { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; font-style: italic; color: #0d47a1; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetim Merkezi")

# --- Dinamik Söz Alanı ---
# Yılın kaçıncı günü olduğunu alarak her gün değişmesini sağlıyoruz
gun_index = datetime.date.today().timetuple().tm_yday % len(motivasyon_sozleri)
st.markdown(f'<div class="soz-kutusu">🌟 <b>Günün Sözü:</b> {motivasyon_sozleri[gun_index]}</div>', unsafe_allow_html=True)

st.markdown("---")

if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = pd.DataFrame(columns=[
        "Tarih", "Saat", "Ad Soyad", "Konu", "Hedef (Saat)", "Gerçekleşen (Saat)", "Başarı (%)"
    ])

# --- Sidebar: Yeni Kayıt ---
with st.sidebar:
    st.header("📝 Yeni Kayıt")
    isim = st.selectbox("Ad Soyad", list(kullanici_sozlugu.keys()))
    
    if isim in kullanici_sozlugu:
        dosya = kullanici_sozlugu[isim]
        if os.path.exists(dosya):
            st.image(dosya, width=100)
    
    with st.form("yeni_kayit", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        saat = st.time_input("Saat", datetime.time(9, 0))
        konu = st.text_input("Konu Başlığı")
        hedef_saat = st.number_input("Hedeflenen Saat", min_value=0.0, step=0.5)
        gercek_saat = st.number_input("Gerçekleşen Saat", min_value=0.0, step=0.5)
        ekle = st.form_submit_button("HEDEFE EKLE 🎯")

    if ekle:
        if konu.strip() == "":
            st.error("Lütfen konu başlığını doldurunuz.")
        else:
            yeni_satir = pd.DataFrame([{
                "Tarih": tarih, "Saat": saat, "Ad Soyad": isim, "Konu": konu,
                "Hedef (Saat)": hedef_saat, "Gerçekleşen (Saat)": gercek_saat,
                "Başarı (%)": round((gercek_saat / hedef_saat * 100) if hedef_saat > 0 else 0, 2)
            }])
            st.session_state.veri_listesi = pd.concat([st.session_state.veri_listesi, yeni_satir], ignore_index=True)
            st.success(f"Harika bir adım attın, {isim}! 🌟")
            st.rerun()

# --- Dashboard ---
st.subheader("📊 İlerleme Paneli")
st.session_state.veri_listesi = st.data_editor(st.session_state.veri_listesi, use_container_width=True)

# İstatistikler ve görseller... (önceki kod ile aynı)
