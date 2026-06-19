import streamlit as st
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Hedef Takip Uygulaması", layout="wide")

# Başlık ve açıklama
st.title("🎯 Kişi ve Hedef Takip Sistemi")
st.write("Kişi bilgilerini ve hedeflerinizi aşağıdan kolayca yönetebilirsiniz.")

# Veriyi saklamak için oturum durumu
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = []

# --- Giriş Formu ---
with st.sidebar:
    st.header("Yeni Kayıt Girişi")
    with st.form("kayit_formu", clear_on_submit=True):
        isim = st.text_input("Ad Soyad")
        konu = st.text_input("Konu Başlığı")
        hedef = st.number_input("Hedef Değer", min_value=0.0, step=0.1)
        gerceklesen = st.number_input("Gerçekleşen Değer", min_value=0.0, step=0.1)
        
        submit = st.form_submit_button("Kaydet")
        
        if submit:
            if isim and konu:
                basari = (gerceklesen / hedef * 100) if hedef > 0 else 0
                st.session_state.veri_listesi.append({
                    "Ad Soyad": isim,
                    "Konu": konu,
                    "Hedef": hedef,
                    "Gerçekleşen": gerceklesen,
                    "Başarı (%)": round(basari, 2)
                })
                st.success(f"{isim} için kayıt eklendi!")
            else:
                st.warning("Lütfen Ad Soyad ve Konu alanlarını doldurunuz.")

# --- Veri Tablosu ---
st.subheader("Kayıtlı Veriler")
if st.session_state.veri_listesi:
    df = pd.DataFrame(st.session_state.veri_listesi)
    st.dataframe(df, use_container_width=True)
    
    # İndirme seçeneği
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Verileri CSV Olarak İndir",
        data=csv,
        file_name='hedef_takip_verileri.csv',
        mime='text/csv',
    )
else:
    st.info("Henüz veri girişi yapılmadı. Yan panelden giriş yapabilirsiniz.")
