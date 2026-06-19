import streamlit as st
import pandas as pd
import datetime

# Sayfa Genişliği ve Ayarları
st.set_page_config(page_title="Başarı Takip", layout="wide")

# --- CSS ile Özel Tema ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #1f77b4; text-align: center; font-family: 'Arial', sans-serif; }
    [data-testid="stMetricValue"] { font-size: 30px !important; color: #2e7d32 !important; }
    div.stButton > button {
        background-color: #4CAF50; color: white; border-radius: 20px;
        border: none; padding: 10px 24px; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #45a049; transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetim Merkezi")
st.markdown("---")

# Session state başlatma (Eğer yoksa boş bir DataFrame oluştur)
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = pd.DataFrame(columns=[
        "Tarih", "Saat", "Ad Soyad", "Konu", "Hedef (Saat)", "Gerçekleşen (Saat)", "Başarı (%)"
    ])

# --- Sidebar: Yeni Kayıt ---
with st.sidebar:
    st.header("📝 Yeni Kayıt")
    with st.form("yeni_kayit", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        saat = st.time_input("Saat", datetime.time(9, 0))
        isim = st.text_input("Ad Soyad")
        konu = st.text_input("Konu Başlığı")
        hedef_saat = st.number_input("Hedeflenen Saat", min_value=0.0, step=0.5)
        gercek_saat = st.number_input("Gerçekleşen Saat", min_value=0.0, step=0.5)
        
        ekle = st.form_submit_button("HEDEFE EKLE 🎯")
        if ekle and isim:
            yeni_satir = pd.DataFrame([{
                "Tarih": tarih,
                "Saat": saat,
                "Ad Soyad": isim,
                "Konu": konu,
                "Hedef (Saat)": hedef_saat,
                "Gerçekleşen (Saat)": gercek_saat,
                "Başarı (%)": round((gercek_saat / hedef_saat * 100) if hedef_saat > 0 else 0, 2)
            }])
            # Yeni veriyi mevcut DataFrame'e ekle
            st.session_state.veri_listesi = pd.concat([st.session_state.veri_listesi, yeni_satir], ignore_index=True)
            st.success("Harika bir adım attın! 🌟")

# --- Dashboard: Veri Düzenleme ---
st.subheader("📊 İlerleme Paneli")
st.write("Tablo üzerinden doğrudan değişiklik yapabilirsin:")

# Veri düzenleyici
edited_df = st.data_editor(st.session_state.veri_listesi, use_container_width=True)
st.session_state.veri_listesi = edited_df

# --- İstatistikler ve Görselleştirme ---
# Hata almamak için güvenli kontrol (isinstance)
if isinstance(st.session_state.veri_listesi, pd.DataFrame) and not st.session_state.veri_listesi.empty:
    st.divider()
    col1, col2 = st.columns(2)
    toplam_hedef = st.session_state.veri_listesi["Hedef (Saat)"].sum()
    toplam_gercek = st.session_state.veri_listesi["Gerçekleşen (Saat)"].sum()
    
    col1.metric("Toplam Hedeflenen", f"{toplam_hedef} Saat")
    col2.metric("Toplam Gerçekleşen", f"{toplam_gercek} Saat")
    
    st.markdown("### Kişisel İlerleme Çubukları")
    for _, row in st.session_state.veri_listesi.iterrows():
        basari = row["Başarı (%)"]
        st.write(f"**{row['Ad Soyad']}** - {row['Konu']}")
        st
