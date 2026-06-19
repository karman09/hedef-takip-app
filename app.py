import streamlit as st
import pandas as pd
import datetime
import os

# Sayfa Genişliği ve Ayarları
st.set_page_config(page_title="Başarı Takip", layout="wide")

# --- Kalıcı Veri Yönetimi ---
DATA_FILE = "veri_kayitlari.csv"

def veri_yukle():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Tarih", "Saat", "Ad Soyad", "Konu", "Hedef (Saat)", "Gerçekleşen (Saat)", "Başarı (%)"
        ])

def veri_kaydet(df):
    df.to_csv(DATA_FILE, index=False)

# --- Motivasyon Sözleri ---
motivasyon_sozleri = [
    "Başarının yolu, denemekten geçer.", "Küçük adımlar, büyük hedeflere götürür.",
    "Bugün, dünden daha fazlasını yapabilirsin.", "Başarı, hazırlık ve fırsatın buluşmasıdır.",
    "Kendine inan, her şeyin yarısını başarmışsın demektir.", "Asla pes etme, büyük şeyler zaman alır.",
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

# --- CSS Stilleri ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .soz-kutusu { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; font-style: italic; color: #0d47a1; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #4CAF50; color: white; border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetimi")

# --- Dinamik Söz Alanı ---
gun_index = datetime.date.today().timetuple().tm_yday % len(motivasyon_sozleri)
st.markdown(f'<div class="soz-kutusu">🌟 <b>Günün Sözü:</b> {motivasyon_sozleri[gun_index]}</div>', unsafe_allow_html=True)

st.markdown("---")

# Verileri dosyadan yükle
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = veri_yukle()

# --- Sidebar: Yeni Kayıt ---
with st.sidebar:
    st.header("📝 Yeni Kayıt")
    
    isim = st.selectbox("Ad Soyad", list(kullanici_sozlugu.keys()))
    
    if isim in kullanici_sozlugu and os.path.exists(kullanici_sozlugu[isim]):
        st.image(kullanici_sozlugu[isim], width=100)
    
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
                "Tarih": str(tarih),
                "Saat": str(saat),
                "Ad Soyad": isim,
                "Konu": konu,
                "Hedef (Saat)": hedef_saat,
                "Gerçekleşen (Saat)": gercek_saat,
                "Başarı (%)": round((gercek_saat / hedef_saat * 100) if hedef_saat > 0 else 0, 2)
            }])
            st.session_state.veri_listesi = pd.concat([st.session_state.veri_listesi, yeni_satir], ignore_index=True)
            
            # Veriyi dosyaya kaydet
            veri_kaydet(st.session_state.veri_listesi)
            
            st.success(f"Harika bir adım attın, {isim}! 🌟")
            st.rerun()

# --- Dashboard ---
st.subheader("📊 İlerleme Paneli")
st.session_state.veri_listesi = st.data_editor(st.session_state.veri_listesi, use_container_width=True)

# Düzenleme yapıldığında dosyayı güncelle
if st.button("Tablo Değişikliklerini Kaydet 💾"):
    veri_kaydet(st.session_state.veri_listesi)
    st.rerun()

if not st.session_state.veri_listesi.empty:
    st.divider()
    st.markdown("### Kişisel İlerleme Çubukları")
    for _, row in st.session_state.veri_listesi.iterrows():
        cols = st.columns([1, 6])
        isim_row = row['Ad Soyad']
        with cols[0]:
            if isim_row in kullanici_sozlugu and os.path.exists(kullanici_sozlugu[isim_row]):
                st.image(kullanici_sozlugu[isim_row], width=50)
        with cols[1]:
            st.write(f"**{isim_row}** - {row['Konu']}")
            st.progress(min(float(row["Başarı (%)"]) / 100, 1.0))
    
    csv = st.session_state.veri_listesi.to_csv(index=False).encode('utf-8')
    st.download_button("Tüm Verileri İndir (CSV) 📥", csv, "hedef_takip.csv", "text/csv")
