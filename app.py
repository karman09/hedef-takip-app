import streamlit as st
import pandas as pd
import datetime
import os # Resim kontrolü için gerekli

# Sayfa Genişliği ve Ayarları
st.set_page_config(page_title="Başarı Takip", layout="wide")

# --- CSS ile Özel Tema ve Resim Stili ---
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
    
    /* İsim alanındaki resmi hizalamak için yeni CSS */
    .user-profile-input {
        display: flex;
        align-items: center;
        gap: 10px; /* Resim ve metin kutusu arasındaki boşluk */
    }
    .user-profile-input img {
        border-radius: 50%; /* Yuvarlak resim */
        border: 2px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetim Merkezi")
st.markdown("---")

# Session state başlatma
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = pd.DataFrame(columns=[
        "Tarih", "Saat", "Ad Soyad", "Konu", "Hedef (Saat)", "Gerçekleşen (Saat)", "Başarı (%)"
    ])

# --- Resim Dosyası Yolu (ÖNEMLİ: Resmi kodla aynı klasöre 'profil.jpg' olarak koyun) ---
image_path = "profil.jpg" # Eğer dosya adı farklıysa burayı değiştirin (örn: 'kevser_profil.png')

# --- Sidebar: Yeni Kayıt ---
with st.sidebar:
    st.header("📝 Yeni Kayıt")
    with st.form("yeni_kayit", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        saat = st.time_input("Saat", datetime.time(9, 0))

        # --- YENİ BÖLÜM: Resim ve İsim Girişi ---
        # Resim ve giriş kutusunu yan yana getirmek için container ve sütunlar
        st.write("**Ad Soyad**") # Etiket formun içinde kalsın
        col_img, col_name = st.columns([1, 4]) # 1 birim resim, 4 birim isim kutusu
        
        with col_img:
            if os.path.exists(image_path):
                # Resmi göster, genişliği sütuna uyarla, yuvarlak yapmak için CSS sınıfı kullan
                st.image(image_path, width=60) # Genişliği ayarlayabilirsiniz
            else:
                st.warning("⚠️ profil.jpg bulunamadı.") # Resim yoksa uyarı ver
                
        with col_name:
            # text_input'un varsayılan etiketini gizliyoruz (st.write ile üstte yazdık)
            isim = st.text_input("", label_visibility="collapsed") 

        konu = st.text_input("Konu Başlığı")
        hedef_saat = st.number_input("Hedeflenen Saat", min_value=0.0, step=0.5)
        gercek_saat = st.number_input("Gerçekleşen Saat", min_value=0.0, step=0.5)
        
        ekle = st.form_submit_button("HEDEFE EKLE 🎯")
        
        # Hatalı/Boş veri girmeyi önlemek için kontrol
        if ekle:
            # 'isim' değişkenini kullanıyoruz (kol_name içindeki text_input'un değeri)
            if isim.strip() == "" or konu.strip() == "":
                st.error("Lütfen Ad Soyad ve Konu alanlarını doldurunuz.")
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
                # pd.concat kullanımı (Pandas 1.4.0+ için güncel)
                st.session_state.veri_listesi = pd.concat([st.session_state.veri_listesi, yeni_satir], ignore_index=True)
                st.success(f"Harika bir adım attın, {isim}! 🌟")

# --- Dashboard: Veri Düzenleme ---
st.subheader("📊 İlerleme Paneli")
st.write("Aşağıdaki tablodan hatalı kayıtları seçip 'Delete' tuşuyla silebilir veya düzenleyebilirsin:")

# Veri düzenleyici
st.session_state.veri_listesi = st.data_editor(st.session_state.veri_listesi, use_container_width=True)

# --- İstatistikler ve Görselleştirme ---
if isinstance(st.session_state.veri_listesi, pd.DataFrame) and not st.session_state.veri_listesi.empty:
    st.divider()
    col1, col2 = st.columns(2)
    toplam_hedef = st.session_state.veri_listesi["Hedef (Saat)"].sum()
    toplam_gercek = st.session_state.veri_listesi["Gerçekleşen (Saat)"].sum()
    
    col1.metric("Toplam Hedeflenen", f"{toplam_hedef} Saat")
    col2.metric("Toplam Gerçekleşen", f"{toplam_gercek} Saat")
    
    st.markdown("### Kişisel İlerleme Çubukları")
    for _, row in st.session_state.veri_listesi.iterrows():
        # Sadece geçerli veri satırlarını göster
        if pd.notna(row['Ad Soyad']):
            basari = row["Başarı (%)"]
            # Buradaki ismin yanına da resim koymak isterseniz:
            col_pb_img, col_pb_text = st.columns([1, 10])
            with col_pb_img:
                 if os.path.exists(image_path):
                     st.image(image_path, width=30)
            with col_pb_text:
                st.write(f"**{row['Ad Soyad']}** - {row['Konu']}")
                st.progress(min(basari / 100, 1.0))
                if basari >= 100:
                    st.caption("✅ Hedef tamamlandı, harikasın!")
    
    # İndirme Butonu
    csv = st.session_state.veri_listesi.to_csv(index=False).encode('utf-8')
    st.download_button("Tüm Verileri İndir (CSV) 📥", csv, "hedef_takip.csv", "text/csv")
