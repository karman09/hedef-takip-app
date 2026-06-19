import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Motivasyonel Hedef Takibi", layout="wide")

# Motivasyon Sözleri
sozler = [
    "Küçük adımlar, büyük zaferlerin başlangıcıdır. 💪",
    "Hedefine odaklan, engellere değil. 🎯",
    "Disiplin, hedefler ile başarı arasındaki köprüdür. 🚀",
    "Bugün yaptığın çalışma, yarınki başarının anahtarıdır. ✨"
]

st.title("🎯 Hedef Takip ve Motivasyon Merkezi")
st.info(f"💡 Günün Motivasyonu: {random.choice(sozler)}")

if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = []

# --- Giriş Formu ---
with st.sidebar:
    st.header("Yeni Kayıt Ekle")
    with st.form("kayit_formu", clear_on_submit=True):
        isim = st.text_input("Ad Soyad")
        konu = st.text_input("Konu Başlığı")
        hedef = st.number_input("Hedef Değer", min_value=0.0, step=0.1)
        gerceklesen = st.number_input("Gerçekleşen Değer", min_value=0.0, step=0.1)
        
        submit = st.form_submit_button("Kaydet")
        
        if submit and isim:
            basari = (gerceklesen / hedef * 100) if hedef > 0 else 0
            st.session_state.veri_listesi.append({
                "Ad Soyad": isim,
                "Konu": konu,
                "Hedef": hedef,
                "Gerçekleşen": gerceklesen,
                "Başarı (%)": round(basari, 2)
            })
            if basari >= 100:
                st.balloons() # Kutlama efekti
                st.success(f"Tebrikler {isim}! Hedefini tamamladın! 🎉")

# --- Dashboard Alanı ---
if st.session_state.veri_listesi:
    # Metrikleri Göster
    df = pd.DataFrame(st.session_state.veri_listesi)
    ortalama_basari = df["Başarı (%)"].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("Kayıtlı Kişi Sayısı", len(df))
    col2.metric("Ortalama Başarı Oranı", f"%{round(ortalama_basari, 1)}")
    
    st.divider()
    
    # İlerleme Çubukları
    st.subheader("İlerleme Durumu")
    for index, row in df.iterrows():
        st.write(f"**{row['Ad Soyad']}** - *{row['Konu']}*")
        progress = min(row['Başarı (%)'] / 100, 1.0)
        st.progress(progress)
        
    st.divider()
    st.dataframe(df, use_container_width=True)
else:
    st.write("Henüz bir hedef eklenmedi. Yan menüden ilk adımı at! ✨")
