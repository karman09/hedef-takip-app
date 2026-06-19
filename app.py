import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Hedef ve Zaman Takibi", layout="wide")

st.title("⏱️ Zaman ve Hedef Yönetim Paneli")

# Oturum Durumu Başlatma
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = pd.DataFrame(columns=["Tarih", "Ad Soyad", "Konu", "Hedef (Saat)", "Gerçekleşen (Saat)", "Başarı (%)"])

# --- Sidebar: Yeni Giriş ---
with st.sidebar:
    st.header("Yeni Kayıt Ekle")
    with st.form("yeni_kayit", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        saat = st.time_input("Saat", datetime.time(9, 0))
        isim = st.text_input("Ad Soyad")
        konu = st.text_input("Konu Başlığı")
        hedef_saat = st.number_input("Günlük Hedef Saat", min_value=0.0, step=0.5)
        gercek_saat = st.number_input("Gerçekleşen Saat", min_value=0.0, step=0.5)
        
        ekle = st.form_submit_button("Ekle")
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
            st.session_state.veri_listesi = pd.concat([st.session_state.veri_listesi, yeni_satir], ignore_index=True)
            st.success("Kayıt Başarılı!")

# --- Dashboard: Düzenleme ve Görünüm ---
st.subheader("Kayıtları Düzenle")
st.write("Aşağıdaki tablodan hücrelere tıklayarak verileri güncelleyebilirsin:")

# st.data_editor ile doğrudan tabloda düzenleme yapma imkanı
edited_df = st.data_editor(st.session_state.veri_listesi, use_container_width=True)

# Düzenlenmiş veriyi session_state'e kaydet
st.session_state.veri_listesi = edited_df

# İstatistikler
if not st.session_state.veri_listesi.empty:
    st.divider()
    col1, col2 = st.columns(2)
    toplam_hedef = st.session_state.veri_listesi["Hedef (Saat)"].sum()
    toplam_gercek = st.session_state.veri_listesi["Gerçekleşen (Saat)"].sum()
    
    col1.metric("Toplam Hedeflenen Saat", f"{toplam_hedef} saat")
    col2.metric("Toplam Gerçekleşen Saat", f"{toplam_gercek} saat")
    
    # İndirme Butonu
    st.download_button("Excel/CSV Olarak İndir", edited_df.to_csv(index=False), "veriler.csv", "text/csv")
